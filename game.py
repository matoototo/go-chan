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
        self.blackPlayer = challenge.challenger
        self.whitePlayer = challenge.challenged
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
                elif (character.upper() == "W"): stones[int(index/19)][index%19] = 2
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
        self.stones = self.__boardString_to_stones()
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
            return 0
        else: return -1
    def __force_make_move (self, move):
            column = ord(move[0].upper())-65
            row = int(move[1:])
            if (self.blackToMove): self.stones[19-row][column] = 1
            else: self.stones[19-row][column] = 2
            self.historyBoardString = self.boardString
            self.boardString = self.__stones_to_boardString()
    def __is_alive (self, move):
        if (self.__find_dead_stones(not self.blackToMove, move)): #suicidal moves only allowed if they capture an opponent's group
            self.__remove_dead_stones(not self.blackToMove)
            return True
        else:
            return not self.__find_dead_stones(self.blackToMove, move)
    def __find_dead_stones (self, isBlack, move):
        def get_friendly_neighbours (row, column, group): #returns adjacent same color stones (4 maximum) and number of liberties
            liberties = 0
            friendly = []
            if row > 0:
                if self.stones[row-1][column] == color and [row-1, column] not in group: friendly.append([row-1, column])
                elif self.stones[row-1][column] == 0: liberties += 1
            if row < 18:
                if self.stones[row+1][column] == color and [row+1, column] not in group: friendly.append([row+1, column])
                elif self.stones[row+1][column] == 0: liberties += 1
            if column > 0:
                if self.stones[row][column-1] == color and [row, column-1] not in group: friendly.append([row, column-1])
                elif self.stones[row][column-1] == 0: liberties += 1
            if column < 18:
                if self.stones[row][column+1] == color and [row, column+1] not in group: friendly.append([row, column+1])
                elif self.stones[row][column+1] == 0: liberties += 1
            friendly.append(liberties)
            return friendly
        """
        Tries move, loops through stones[][] and finds groups with no liberties of a particular color
        If found, returns an array with dead stone indices, else return False
        """
        dead = []
        checked = []
        if (isBlack): color = 1
        else: color = 2
        savedStoneColumn = ord(move[0].upper())-65
        savedStoneRow = int(move[1:])
        savedStone = self.stones[19-savedStoneRow][savedStoneColumn]
        self.__force_make_move(move)
        for row, array in enumerate(self.stones):
            for column, stone in enumerate(array):
                queue = [] #neighbour queue
                group = [[row, column]] #current group
                groupIsAlive = False
                if ([row, column] not in checked):
                    if (stone == color):
                        neighbours = get_friendly_neighbours(row, column, group)
                        queue = neighbours[:-1]
                        if (neighbours[-1]) != 0: groupIsAlive = True
                        while (queue != []):
                            _row, _column = queue.pop(0) 
                            _neighbours = get_friendly_neighbours(_row, _column, group)
                            queue += _neighbours[:-1]
                            if (_neighbours[-1]) != 0: groupIsAlive = True
                            group.append([_row, _column])
                    if not groupIsAlive and stone == color:
                        dead += group
                    checked += group
        self.stones[19-savedStoneRow][savedStoneColumn] = savedStone
        if (dead != []): return dead
        else: return False
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
