class Game:
    """
    boardString = FEN-like presentation of the board:
        - 3 different types of characters:
            - W: white stone
            - B: black stone
            - number: number of blanks
        - each character is divided by a space
        - example:
            - 19x19 start position: "361"
            - 19x19 with a black stone on D16: "60 B 300"
    """
    def __init__ (self, challenge):
        self.challenge = challenge
        self.boardString = str(self.challenge.boardSize**2)
        self.stones = self.__boardString_to_stones()
        self.blackToMove = True
    def __boardString_to_stones (self):
        stones = [[0 for column in range(self.challenge.boardSize)] for row in range(self.challenge.boardSize)]
        #stones = [[0]*self.challenge.boardSize]*self.challenge.boardSize #set stones to 0
        index = 0
        for character in self.boardString.split():
            try:
                numberOfBlanks = int(character)
                index += numberOfBlanks
            except:
                if   (character.lower() == "b"): stones[int(index/19)][index%19] = 1
                elif (character.lower() == "w"): stones[int(index/19)][index%19] = 2
                index += 1
        return stones
    def __stones_to_boardString (self):
        boardString = ""
        blanks = 0
        for stone_list in self.stones:
            for stone in stone_list:
                if (stone == 0): blanks += 1
                else:
                    if (blanks != 0): boardString += f" {str(blanks)}"
                    if (stone == 1): boardString += " b"
                    if (stone == 2): boardString += " w"
                    blanks = 0
        if (blanks != 0): boardString += f" {str(blanks)}"
        return boardString[1:]
    def set_boardString (self, newBoardString):
        self.boardString = newBoardString
        return 0
    def make_move (self, move):
        if (self.__is_legal(move)):
            column = ord(move[0].upper())-65
            row = int(move[1:])
            if (self.blackToMove): self.stones[19-row][column] = 1
            else: self.stones[19-row][column] = 2
            self.blackToMove = not self.blackToMove
            self.boardString = self.__stones_to_boardString()
        else: return -1
    def __is_legal (self, move):
        return True
class Challenge:
    def __init__ (self, challenger, challenged, boardSize):
        self.challenger = challenger
        self.challenged = challenged
        self.boardSize = boardSize
    def __copy__ (self):
        return Challenge(self.challenger, self.challenged, self.boardSize)