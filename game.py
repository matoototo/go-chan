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
        self.blackPlayer = challenge.playerChallenger
        self.whitePlayer = challenge.playerChallenged
        self.boardSize = challenge.boardSize
        self.boardString = str(self.boardSize ** 2)
        self.stones = self.__boardString_to_stones()
        self.blackToMove = True
        self.historyBoardString = self.boardString
        self.moves = []
        self.passCounter = 0
        self.prisoners = [0, 0] #B, W (refers to the number of points B (W) will get from prisoners, not the number of 'dead' (imprisoned) B (W) stones)
        self.winner = False

    def __boardString_to_stones (self):
        stones = [[0 for column in range(self.boardSize)] for row in range(self.boardSize)]
        index = 0

        for character in self.boardString.split():
            try:
                numberOfBlanks = int(character)
                index += numberOfBlanks
            except:
                if   (character.upper() == "B"): stones[int(index / self.boardSize)][index % self.boardSize] = 1
                elif (character.upper() == "W"): stones[int(index / self.boardSize)][index % self.boardSize] = 2
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
                    elif (stone == 2): boardString += " W"

                    blanks = 0
        if (blanks != 0): boardString += f" {str(blanks)}"
        return boardString[1:]

    def set_boardString (self, newBoardString):
        self.boardString = newBoardString
        self.stones = self.__boardString_to_stones()
        return 0

    def make_move (self, move):
        if (self.__is_alive(move)):
            if (move != "pass"):
                if (move == "resign"):
                    if (self.blackToMove): self.end_game("white")
                    else: self.end_game("black")
                    return 0

                self.passCounter = 0
                column = ord(move[0].upper()) - 65
                row = int(move[1:])

                if (self.blackToMove): self.stones[self.boardSize-row][column] = 1
                else: self.stones[self.boardSize-row][column] = 2
            else:
                self.passCounter += 1

                if (self.passCounter == 2):
                    self.end_game("pass")
                    return 0

            self.blackToMove = not self.blackToMove
            self.historyBoardString = self.boardString
            self.boardString = self.__stones_to_boardString()
            self.moves.append(move)

            return 0
        else: return -1

    def __force_make_move (self, move):
            column = ord(move[0].upper()) - 65
            row = int(move[1:])

            if (self.blackToMove): self.stones[self.boardSize-row][column] = 1
            else: self.stones[self.boardSize - row][column] = 2

            self.historyBoardString = self.boardString
            self.boardString = self.__stones_to_boardString()

    def __is_alive (self, move):
        if (move != "pass"):
            if (self.__find_dead_stones(not self.blackToMove, move)): #suicidal moves only allowed if they capture an opponent's group
                self.__remove_dead_stones(not self.blackToMove, move)
                return True
            else:
                return not self.__find_dead_stones(self.blackToMove, move)
        else:
            return True

    def __find_dead_stones (self, isBlack, move):
        """
        Tries move, loops through stones[][] and finds groups with no liberties of a particular color
        If found, returns an array with dead stone indices, else return False
        """

        def get_friendly_neighbours (row, column, group): #returns adjacent same color stones (4 maximum) and number of liberties
            liberties = 0
            friendly = []

            if row > 0:
                if self.stones[row - 1][column] == color and [row - 1, column] not in group: friendly.append([row - 1, column])
                elif self.stones[row - 1][column] == 0: liberties += 1
            if row < self.boardSize - 1:
                if self.stones[row + 1][column] == color and [row + 1, column] not in group: friendly.append([row + 1, column])
                elif self.stones[row+1][column] == 0: liberties += 1
            if column > 0:
                if self.stones[row][column - 1] == color and [row, column - 1] not in group: friendly.append([row, column - 1])
                elif self.stones[row][column - 1] == 0: liberties += 1
            if column < self.boardSize - 1:
                if self.stones[row][column + 1] == color and [row, column + 1] not in group: friendly.append([row, column + 1])
                elif self.stones[row][column + 1] == 0: liberties += 1

            friendly.append(liberties)
            return friendly

        dead = []
        checked = []

        if (isBlack): color = 1
        else: color = 2

        savedStoneColumn = ord(move[0].upper())-65
        savedStoneRow = int(move[1:])
        savedStone = self.stones[self.boardSize-savedStoneRow][savedStoneColumn]
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

        self.stones[self.boardSize-savedStoneRow][savedStoneColumn] = savedStone

        if (dead != []): return dead
        else: return False

    def __remove_dead_stones(self, isBlack, move):
        """
        Calls __find_dead_stones() and removes the returned dead stones
        """

        stones = self.__find_dead_stones(isBlack, move)
        if stones:
            for stone in stones:
                self.stones[stone[0]][stone[1]] = 0

                if (isBlack): self.prisoners[1] += 1
                else: self.prisoners[0] += 1

    def draw_goban (self):
        goban = VisualBoard(self.boardSize)
        goban.generate_image(self.stones).save("goban.png")

    def end_game (self, winner = False):
        """
        Notify players that the game is over, provide them with prisoner count and wait for territory information.
        """

        if (winner in ["black", "white"]):
            if (winner == "black"):
                self.winner = self.blackPlayer
            else: self.winner = self.whitePlayer
        else:
            self.winner = self.blackPlayer #TEMPORARY, winner by counting stones has yet to be implemented!

        self.blackPlayer.finish_game()
        self.whitePlayer.finish_game()

    def set_players(self, blackPlayer = False, whitePlayer = False):
        if (blackPlayer): self.blackPlayer = blackPlayer
        if (whitePlayer): self.whitePlayer = whitePlayer
class Challenge:
    def __init__ (self, challenger, challenged, boardSize, playerChallenger = False, playerChallenged = False):
        self.challenger = challenger
        self.challenged = challenged
        self.boardSize = boardSize
        self.playerChallenger = playerChallenger
        self.playerChallenged = playerChallenged

    def __copy__ (self):
        return Challenge(self.challenger, self.challenged, self.boardSize, self.playerChallenger, self.playerChallenger)
