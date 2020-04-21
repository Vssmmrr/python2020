class Command:
    def __init__(self):
        self.is_completed = False

    def complete(self):
        self.is_completed = True

    def undo(self):
        self.is_completed = False


class Move(Command):
    def __init__(self, draught, new_x, new_y):
        super().__init__()
        self.draught = draught
        self.new_x = new_x
        self.new_y = new_y
        self.old_x = None
        self.old_y = None

    def complete(self):
        super().complete()
        self.old_x = self.draught.x
        self.old_y = self.draught.y
        self.draught.field[self.old_y][self.old_x] = None
        self.draught.field[self.new_y][self.new_x] = self.draught
        self.draught.x = self.new_x
        self.draught.y = self.new_y

    def undo(self):
        super().undo()
        self.draught.x = self.old_x
        self.draught.y = self.old_y
        self.draught.field[self.new_y][self.new_x] = None
        self.draught.field[self.old_y][self.old_x] = self.draught


class Remove(Command):
    def __init__(self, draught):
        super().__init__()
        self.draught = draught

    def complete(self):
        super().complete()
        self.draught.field[self.draught.y][self.draught.x] = None
        if self.draught.color == self.draught.field.WHITE:
            self.draught.field.num_white_draughts -= 1
        else:
            self.draught.field.num_black_draughts -= 1

    def undo(self):
        super().undo()
        self.draught.field[self.draught.y][self.draught.x] = self.draught
        if self.draught.color == self.draught.field.WHITE:
            self.draught.field.num_white_draughts += 1
        else:
            self.draught.field.num_black_draughts += 1
            

class MakeKing(Command):
    def __init__(self, draught):
        super().__init__()
        self.draught = draught

    def complete(self):
        super().complete()
        self.draught.is_king = True

    def undo(self):
        super().undo()
        self.draught.is_king = False
