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
                name TEXT NOT NULL UNIQUE
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY,
                player1_id INTEGER,
                player2_id INTEGER,
                FOREIGN KEY(player1_id) REFERENCES players(id),
                FOREIGN KEY(player2_id) REFERENCES players(id)
            )
        """)
        self.conn.commit()

    def __encode_name(self, player):
        """Encodes the given player name to ensure that special characters don't destroy our SQL queries or tables.

        Arguments:
        player -- The player name
        """
        bytestring = bytes(player, "utf-8")

        return base64.b64encode(bytestring)

    def __player_id(self, player):
        """Returns the player id for a given player name.
        
        Arguments:
        player -- The player name
        """

        encodedName = self.__encode_name(player)
        c = self.conn.cursor()

        c.execute("""
            INSERT OR IGNORE INTO players (name)
            VALUES (?)
        """, (encodedName,))
        c.execute("""
            SELECT id
            FROM players
            WHERE name = ?
        """, (encodedName,))

        playerId = c.fetchone()

        self.conn.commit()

        return playerId[0]

    def games_played(self, player):
        """Returns the amount of games a player has played.

        Arguments:
        player -- The player
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
        player -- The player
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
        player -- The player
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

    def log_game(self, player1, player2):
        """Adds a win to the specified player's stats.

        Arguments:
        player1 -- The winner
        player2 -- The loser
        """

        player1Id = self.__player_id(player1)
        player2Id = self.__player_id(player2)
        c = self.conn.cursor()

        c.execute("""
            INSERT INTO games (player1_id, player2_id)
            VALUES (?, ?)
        """, (player1Id, player2Id))

        self.conn.commit()

#storage = StatStorage("test.db")
#storage.log_game("A", "B")
#storage.log_game("A", "B")
#storage.log_game("B", "A")
#storage.log_game("A", "B")
#storage.log_game("B", "A")
#storage.log_game("B", "A")
#stats = storage.wins("A")
#print(stats)
