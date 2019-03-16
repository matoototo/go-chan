import sqlite3
import base64

class StatStorage:
    """A class to log and retrieve match data like wins, losses or games played.
    Uses an SQLite database.
    """

    def __init__(self, path):
        """Initializes a new database at the given path."""

        self.conn = sqlite3.connect(path)

        c = self.conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                discord_id TEXT NOT NULL UNIQUE,
                elo INTEGER DEFAULT 1000
            )
        """)

        c.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                player1_id INTEGER,
                player2_id INTEGER,
                board_size INTEGER,
                moves TEXT,
                FOREIGN KEY(player1_id) REFERENCES players(id),
                FOREIGN KEY(player2_id) REFERENCES players(id)
            )
        """)

        self.conn.commit()


    def __encode_name(self, player):
        """Encodes the player name from a given player object to ensure that special characters don't destroy our SQL queries or tables.

        Arguments:
        player -- The player object
        """
        bytestring = bytes(player.name, "utf-8")
        return base64.b64encode(bytestring)


    def __decode_name(self, encoded):
        return base64.b64decode("".join(map(chr,encoded))).decode('utf-8')


    def __player_id(self, player):
        """Returns the player id for a given player object.
        
        Arguments:
        player -- The player object
        """

        encodedName = self.__encode_name(player)
        c = self.conn.cursor()

        c.execute("""
            INSERT OR IGNORE INTO players (name, discord_id)
            VALUES (?, ?)
        """, (encodedName, player.id))

        c.execute("""
            SELECT id
            FROM players
            WHERE discord_id = ?
        """, (player.id,))

        playerId = c.fetchone()
        self.conn.commit()

        return playerId[0]


    def games_played(self, player):
        """Returns the amount of games a player has played.

        Arguments:
        player -- The player object
        """

        playerId = self.__player_id(player)
        c = self.conn.cursor()

        c.execute("""
            SELECT COUNT(games.id)
            FROM games
            WHERE player1_id = ? OR player2_id = ?
        """, (playerId, playerId))

        gameCount = c.fetchone()
        self.conn.commit()

        return gameCount[0]


    def wins(self, player):
        """Returns the amount of games a player has won.

        Arguments:
        player -- The player object
        """

        playerId = self.__player_id(player)
        c = self.conn.cursor()

        c.execute("""
            SELECT COUNT(games.id)
            FROM games
            WHERE player1_id = ?
        """, (playerId,))

        winCount = c.fetchone()
        self.conn.commit()

        return winCount[0]


    def losses(self, player):
        """Returns the amount of games a player has lost.

        Arguments:
        player -- The player object
        """

        playerId = self.__player_id(player)
        c = self.conn.cursor()

        c.execute("""
            SELECT COUNT(games.id)
            FROM games
            WHERE player2_id = ?
        """, (playerId,))

        lossCount = c.fetchone()
        self.conn.commit()

        return lossCount[0]


    def stats_vs(self, player1, player2):
        """Returns the wins and losses between two players.
        The return value is an array of the form [p1wins, p2wins].

        Arguments:
        player1 -- The first player object
        player2 -- The second player object
        """

        player1Id = self.__player_id(player1)
        player2Id = self.__player_id(player2)
        c = self.conn.cursor()

        c.execute("""
            SELECT COUNT(games.id)
            FROM games
            WHERE player1_id = ? AND player2_id = ?
        """, (player1Id, player2Id))

        player1WinCount = c.fetchone()

        c.execute("""
            SELECT COUNT(games.id)
            FROM games
            WHERE player1_id = ? AND player2_id = ?
        """, (player2Id, player1Id))

        player2WinCount = c.fetchone()
        self.conn.commit()

        return [player1WinCount[0], player2WinCount[0]]


    def log_game(self, player1, player2, boardSize, moveString):
        """Adds a win to the specified player's stats.

        Arguments:
        player1 -- The winner player object
        player2 -- The loser player object
        """

        player1Id = self.__player_id(player1)
        player2Id = self.__player_id(player2)
        c = self.conn.cursor()

        c.execute("""
            INSERT INTO games (player1_id, player2_id, board_size, moves)
            VALUES (?, ?, ?, ?)
        """, (player1Id, player2Id, boardSize, moveString))

        self.__update_elo(player1, player2)

        self.conn.commit()
    

    def get_elo(self, player):
        """Returns the current Elo rating of the specified player

        Arguments:
        player -- Player object
        """

        playerId = self.__player_id(player)
        c = self.conn.cursor()

        c.execute("""
            SELECT elo FROM players
            WHERE id = ?
        """, (playerId,))

        return c.fetchone()[0]


    def __update_elo(self, winner, loser):
        """Updates Elo ratings of given players

        Arguments:
        winner -- Player object of the winner
        loser -- Player object of the loser
        """

        winnerElo = self.get_elo(winner)
        loserElo = self.get_elo(loser)

        player1Id = self.__player_id(winner)
        player2Id = self.__player_id(loser)

        expectedScore = 1/(1+10**((loserElo-winnerElo)/400)) #for winner
        
        if (winnerElo < 2100): kWinner = 32
        elif (winnerElo <= 2400): kWinner = 24
        else: kWinner = 16
        
        if (loserElo < 2100): kLoser = 32
        elif (loserElo <= 2400): kLoser = 24
        else: kLoser = 16

        winnerElo += round(kWinner*(1-expectedScore), 2)
        loserElo += round(kLoser*(-expectedScore), 2)

        c = self.conn.cursor()

        c.execute("""
            UPDATE players
            SET elo = ?
            WHERE id = ?
        """, (winnerElo, player1Id))
        
        c.execute("""
            UPDATE players
            SET elo = ?
            WHERE id = ?
        """, (loserElo, player2Id))

        self.conn.commit()