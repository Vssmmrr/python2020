import numpy as np
import pygame
import pygame.gfxdraw
from command import MakeKing, Move, Remove


class Draught:
    def __init__(self, field, x, y, is_white):
        self.x = x
        self.y = y
        self.is_white = is_white
        self.is_king = False
        self.field = field

    def move(self, dx, dy):
        # Validate
        if abs(dx) != abs(dy):
            return []
        if not self.is_king:
            y_direction = 1 if self.is_white else -1
            if dy != y_direction and dy != 2 * y_direction and dy != -2 * y_direction:
                return []

        command_list = []
        if abs(dx) > 1:
            # Check that there is only one draught on the way
            dir_x = dx // abs(dx)
            dir_y = dy // abs(dy)
            cnt_eaten = 0
            for i in range(1, abs(dx)):
                if self.field[self.y + dir_y * i, self.x + dir_x * i]:
                    cnt_eaten += 1
                    command_list.append(Remove(self.field[self.y + dir_y * i, self.x + dir_x * i]))
            if cnt_eaten > 1:
                return []
            elif not self.is_king and cnt_eaten == 0:
                return []

        if self.field[self.y + dy, self.x + dx]:
            return []

        command_list.append(Move(self, self.x + dx, self.y + dy))

        king_side = 7 if self.is_white else 0
        if self.y + dy == king_side and not self.is_king:
            command_list.append(MakeKing(self))
        return command_list

    def can_eat(self):
        return len(self.get_possible_moves(True)) > 0

    def get_possible_moves_draught(self, needs_eating: bool):
        moves = []
        if needs_eating:
            directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            for dx, dy in directions:
                eat_x = self.x + dx
                eat_y = self.y + dy
                dest_x = eat_x + dx
                dest_y = eat_y + dy
                if 0 <= eat_x < 8 and 0 <= eat_y < 8 and 0 <= dest_x < 8 and 0 <= dest_y < 8 and \
                        self.field[eat_y, eat_x] and self.field[eat_y, eat_x].is_white != self.is_white and \
                        self.field[dest_y, dest_x] is None:
                    moves.append((self, dest_x, dest_y))
        else:
            dy = 1 if self.is_white else -1
            for dx in [1, -1]:
                dest_x = self.x + dx
                dest_y = self.y + dy
                if 0 <= dest_x < 8 and 0 <= dest_y < 8 and self.field[dest_y, dest_x] is None:
                    moves.append((self, dest_x, dest_y))
        return moves

    def get_possible_moves_king(self, needs_eating: bool):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        needed_eaten = 1 if needs_eating else 0
        for dir_x, dir_y in directions:
            cnt_eaten = 0
            for step in range(1, 8):
                new_x = self.x + dir_x * step
                new_y = self.y + dir_y * step
                if new_x < 0 or new_x > 7 or new_y < 0 or new_y > 7:
                    break
                if self.field[new_y, new_x] is not None:
                    if self.field[new_y, new_x].is_white == self.is_white:
                        break
                    else:
                        cnt_eaten += 1
                        if cnt_eaten > needs_eating:
                            break
                        else:
                            continue
                elif cnt_eaten == needed_eaten:
                    moves.append((self, new_x, new_y))
        return moves

    def get_possible_moves(self, needs_eating: bool):
        if self.is_king:
            return self.get_possible_moves_king(needs_eating)
        else:
            return self.get_possible_moves_draught(needs_eating)


class DraughtsField:
    def __init__(self):
        self.field = np.full((8, 8), None)
        self.is_order_white = True
        self.num_white_draughts = 0
        self.num_black_draughts = 0

    def place_default(self):
        self.num_white_draughts = 0
        self.num_black_draughts = 0
        self.field = np.full((8, 8), None)

        # Place draughts
        for i in range(3):
            offset = 1 if i % 2 != 0 else 0
            for j in range(4):
                self.place_draught(j * 2 + offset, i, True)
        for i in range(3):
            offset = 1 if i % 2 == 0 else 0
            for j in range(4):
                self.place_draught(j * 2 + offset, 7 - i, False)

    def place_draught(self, x, y, is_white):
        self[y, x] = Draught(self, x, y, is_white)
        if is_white:
            self.num_white_draughts += 1
        else:
            self.num_black_draughts += 1

    def can_eat(self):
        for y in range(8):
            for x in range(8):
                if self[y, x] is not None and self[y, x].is_white == self.is_order_white and self[y, x].can_eat():
                    return True
        return False

    def get_possible_moves(self):
        needs_eating = self.can_eat()

        moves = []
        for y in range(8):
            for x in range(8):
                if self[y, x] is not None and self[y, x].is_white == self.is_order_white:
                    moves.extend(self[y, x].get_possible_moves(needs_eating))

        return moves

    def switch_order(self):
        self.is_order_white = not self.is_order_white

    def __getitem__(self, key):
        return self.field[key]

    def __setitem__(self, key, value):
        self.field[key] = value

    def complete_command_list(self, cmd_list: list):
        num_draughts = self.num_black_draughts + self.num_white_draughts
        for cmd in cmd_list:
            cmd.complete()
        return num_draughts - self.num_white_draughts - self.num_black_draughts

    def undo_command_list(self, cmd_list: list):
        num_draughts = self.num_black_draughts + self.num_white_draughts
        for cmd in cmd_list[::-1]:
            cmd.undo()
        return self.num_white_draughts + self.num_black_draughts - num_draughts

    def save(self):
        with open('field.txt', 'wt') as f:
            for i in range(8):
                for j in range(8):
                    if self[i, j] is not None:
                        color = 'white' if self[i, j].is_white else 'black'
                        if self[i, j].is_king:
                            color += ' king'
                        f.write(color + '\n')
                    else:
                        f.write('empty\n')
            f.write('white' if self.is_order_white else 'black')

    def load(self):
        with open('field.txt', 'rt') as f:
            lines = f.readlines()
        self.field = np.full((8, 8), None)
        for i in range(8):
            for j in range(8):
                inp = lines[i * 8 + j].split()
                if inp[0] == 'empty':
                    continue
                is_white = (inp[0] == 'white')
                self.place_draught(j, i, is_white)
                if len(inp) > 1:
                    self[i, j].is_king = True
        self.is_order_white = lines[-1].startswith('white')

    def game_over(self):
        return self.num_white_draughts == 0 or self.num_black_draughts == 0


class FieldDrawer:
    WHITE = (255, 233, 185)
    BLACK = (71, 52, 2)
    CELL_SIZE = 60
    CELL_LIGHT = (255, 210, 100)
    CELL_DARK = (160, 105, 30)

    def __init__(self, field: DraughtsField):
        self.field = field

    def draw(self, win):
        for i in range(8):
            for j in range(8):
                color = self.CELL_DARK if (i + j) % 2 == 0 else self.CELL_LIGHT
                x = j * self.CELL_SIZE
                y = (7 - i) * self.CELL_SIZE
                pygame.draw.rect(win, color, (x, y, self.CELL_SIZE, self.CELL_SIZE))

                if self.field[i, j]:
                    color = self.WHITE if self.field[i, j].is_white else self.BLACK
                    pygame.gfxdraw.filled_circle(win, x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2,
                                                 self.CELL_SIZE // 3, color)
                    border_color = (0, 0, 0)
                    if self.field[i, j].is_king:
                        border_color = (255, 215, 0)
                    pygame.gfxdraw.aacircle(win, x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2,
                                            self.CELL_SIZE // 3, border_color)
