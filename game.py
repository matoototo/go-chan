from draw import VisualBoard
class Game:
    """
    boardString = FEN-like presentation of the board:
        - 3 different types of characters:
            - W: white stone
            - B: black stone
            - number: number of blanks
        - the characters are separated by a space
        - example:
            - 19x19 start position: "361"
            - 19x19 with a black stone on D16: "60 B 300"
    """
    def __init__ (self, challenge):
        self.challenge = challenge
        self.boardString = str(self.challenge.boardSize**2)
        self.stones = self.__boardString_to_stones()
        self.blackToMove = True
        self.historyBoardString = self.boardString
    def __boardString_to_stones (self):
        stones = [[0 for column in range(self.challenge.boardSize)] for row in range(self.challenge.boardSize)]
        index = 0
        for character in self.boardString.split():
            try:
                numberOfBlanks = int(character)
                index += numberOfBlanks
            except:
                if   (character.upper() == "B"): stones[int(index/19)][index%19] = 1
                elif (character.upper() == "w"): stones[int(index/19)][index%19] = 2
                index += 1
        return stones
    def __stones_to_boardString (self):
        boardString = ""
        blanks = 0
        for stoneList in self.stones:
            for stone in stoneList:
                if (stone == 0): blanks += 1
                else:
                    if (blanks != 0): boardString += f" {str(blanks)}"
                    if (stone == 1): boardString += " B"
                    if (stone == 2): boardString += " W"
                    blanks = 0
        if (blanks != 0): boardString += f" {str(blanks)}"
        return boardString[1:]
    def set_boardString (self, newBoardString):
        self.boardString = newBoardString
        return 0
    def make_move (self, move):
        if (self.__is_alive(move)):
            column = ord(move[0].upper())-65
            row = int(move[1:])
            if (self.blackToMove): self.stones[19-row][column] = 1
            else: self.stones[19-row][column] = 2
            self.blackToMove = not self.blackToMove
            self.historyBoardString = self.boardString
            self.boardString = self.__stones_to_boardString()
        else: return -1
    def __is_alive (self, move):
        if (self.__find_dead_stones(not self.blackToMove, move)): #suicidal moves only allowed if they capture an opponent's group
            self.__remove_dead_stones(not self.blackToMove)
            return True
        else:
            return not self.__fill_dead_stones(self.blackToMove, move)
    def __find_dead_stones (self, isBlack, move):
        """
        Tries move, loops through stones[][] and finds groups with no liberties of a particular color
        If found, returns an array with dead stone indices, else return False
        """
        return False
    def __remove_dead_stones(self, isBlack):
        """
        Calls __find_dead_stones() and removes the returned dead stones
        """
    def draw_goban (self):
        goban = VisualBoard(self.challenge.boardSize)
        goban.generate_image(self.stones).save("goban.png")
class Challenge:
    def __init__ (self, challenger, challenged, boardSize):
        self.challenger = challenger
        self.challenged = challenged
        self.boardSize = boardSize
    def __copy__ (self):
        return Challenge(self.challenger, self.challenged, self.boardSize)