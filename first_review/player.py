from game import DraughtsField, FieldDrawer
import pygame


class Player:
    def __init__(self, field: DraughtsField, is_order_white):
        self.field = field
        self.is_order_white = is_order_white

    def obtain_events(self, events):
        return False


class InteractivePlayer(Player):
    def __init__(self, field: DraughtsField, is_order_white, cell_size: int):
        super().__init__(field, is_order_white)
        self.focused_draught = None
        self.already_eaten = False
        self.cell_size = cell_size

    def obtain_events(self, events):
        if self.is_order_white != self.field.is_order_white:
            return
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                cell_y = 7 - event.pos[1] // self.cell_size
                cell_x = event.pos[0] // self.cell_size
                if self.focused_draught is None:
                    new_draught = self.field[cell_y, cell_x]
                    if new_draught is not None and new_draught.is_white == self.is_order_white:
                        self.focused_draught = self.field[cell_y, cell_x]
                else:
                    can_eat = self.field.can_eat()
                    cmd_list = self.focused_draught.move(cell_x - self.focused_draught.x,
                                                         cell_y - self.focused_draught.y)
                    if len(cmd_list) > 0:
                        num_eaten = self.field.complete_command_list(cmd_list)
                        if num_eaten > 0:
                            self.already_eaten = True
                        if can_eat and num_eaten == 0:
                            self.field.undo_command_list(cmd_list)
                            if not self.already_eaten:
                                self.focused_draught = None
                            return False
                        elif num_eaten == 0 or not self.focused_draught.can_eat():
                            self.focused_draught = None
                            self.field.switch_order()
                            self.already_eaten = False
                        return True
                    elif not self.already_eaten:
                        self.focused_draught = None
        return False
                    

class AIPlayer(Player):
    EASY = 1
    MEDIUM = 2
    HARD = 3

    def __init__(self, field: DraughtsField, is_order_white, num_predicted_moves: int):
        super().__init__(field, is_order_white)
        self.num_predicted_moves = num_predicted_moves
        self.moved_draught = None

    def get_draughts_difference(self):
        if self.is_order_white:
            return self.field.num_white_draughts - self.field.num_black_draughts
        else:
            return self.field.num_black_draughts - self.field.num_white_draughts

    def best_move_for(self, moves_cnt, draught=None):
        if moves_cnt == 0 or self.field.game_over():
            return self.get_draughts_difference(), None
        if draught:
            moves = draught.get_possible_moves(True)
        else:
            moves = self.field.get_possible_moves()
        best_diff = -9
        best_move = None
        for draught, new_x, new_y in moves:
            cmd_list = draught.move(new_x - draught.x, new_y - draught.y)
            num_eaten = self.field.complete_command_list(cmd_list)
            if num_eaten > 0 and draught.can_eat():
                diff, move = self.best_move_for(moves_cnt, draught)
            else:
                self.field.switch_order()
                diff = self.best_move_against(moves_cnt)
                self.field.switch_order()
            if diff > best_diff:
                best_diff = diff
                best_move = (draught, new_x, new_y)
            self.field.undo_command_list(cmd_list)

        return best_diff, best_move

    def best_move_against(self, moves_cnt, draught=None):
        if moves_cnt == 0 or self.field.game_over():
            return self.get_draughts_difference()
        if draught:
            moves = draught.get_possible_moves(True)
        else:
            moves = self.field.get_possible_moves()
        best_diff = 9
        for draught, new_x, new_y in moves:
            cmd_list = draught.move(new_x - draught.x, new_y - draught.y)
            num_eaten = self.field.complete_command_list(cmd_list)
            if num_eaten > 0 and draught.can_eat():
                diff = self.best_move_against(moves_cnt, draught)
            else:
                self.field.switch_order()
                diff, move = self.best_move_for(moves_cnt - 1)
                self.field.switch_order()
            if diff < best_diff:
                best_diff = diff
            self.field.undo_command_list(cmd_list)
        return best_diff

    def obtain_events(self, events):
        if self.is_order_white != self.field.is_order_white:
            return

        # print("Start move")
        # start = time.clock()
        diff, best_move = self.best_move_for(self.num_predicted_moves, self.moved_draught)
        if best_move is None:
            best_move = self.field.get_possible_moves()[0]
        draught, new_x, new_y = best_move
        cmd_list = draught.move(new_x - draught.x, new_y - draught.y)
        num_eaten = self.field.complete_command_list(cmd_list)
        if num_eaten > 0 and draught.can_eat():
            self.moved_draught = draught
        else:
            self.moved_draught = None
            self.field.switch_order()
        # print("Move: {} seconds".format(time.clock() - start))
        return True
