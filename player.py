class Player:
    def __init__(self, playerID, game = False):
        self.id = playerID
        self.currentGame = game
        self.previousGames = []

    def set_currentGame(self, game):
        self.currentGame = game

    def finish_game(self):
        self.previousGames.append(self.currentGame)
        self.currentGame = False
