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
        self.boardString = self.challenge.boardSize**2
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
    def set_boardString (self, newBoardString):
        self.boardString = newBoardString
        return 0
    

class Challenge:
    def __init__ (self, challenger, challenged, boardSize):
        self.challenger = challenger
        self.challenged = challenged
        self.boardSize = boardSize
    def __copy__ (self):
        return Challenge(self.challenger, self.challenged, self.boardSize)