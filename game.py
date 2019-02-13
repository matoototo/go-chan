class Game:
    #size = board size
    #unique = sum of the player ids
    def __init__ (self, size, unique):
        self.size = size
        self.unique = unique

class Challenge:
    def __init__ (self, challenger, challenged, boardSize):
        self.challenger = challenger
        self.challenged = challenged
        self.boardSize = boardSize
    def __copy__ (self):
        return Challenge(self.challenger, self.challenged, self.boardSize)