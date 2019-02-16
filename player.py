class Player:
    def __init__ (self, playerID, game=False):
        self.id = playerID
        self.currentGame = game
        self.previousGames = []
