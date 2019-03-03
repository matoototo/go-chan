#id 545306487191240704
#token NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8
#perm 523328

import discord
from game import Game, Challenge
from player import Player
from stats import StatStorage

HELP_MESSAGE = discord.Embed(title = "Commands", colour = 0x55cc55, description = "No prefix needed")
HELP_MESSAGE.add_field(name = "`challenge @name <9|13|19>`", value = "Challenge @name", inline = False)
HELP_MESSAGE.add_field(name = "`accept @name`", value = "Accept @name's challenge", inline = False)
HELP_MESSAGE.add_field(name = "`decline @name`", value = "Decline @name's challenge", inline = False)
HELP_MESSAGE.add_field(name = "`move <move> | pass | resign`", value = "Make a move or pass", inline = False)
HELP_MESSAGE.add_field(name = "`withdraw @name`", value = "Withdraw a challenge", inline = False)
HELP_MESSAGE.add_field(name = "`gorules`", value = "Print the Go rules", inline = False)
HELP_MESSAGE.add_field(name = "`kohelp`", value = "Explains ko rule", inline = False)
HELP_MESSAGE.add_field(name = "`gohelp`", value = "Print this help text", inline = False)

client = discord.Client()
stats = StatStorage("stats.db")
commands = ["accept", "challenge", "decline", "move", "withdraw", "gohelp", "gorules", "kohelp", "stats"]
boardSizes = ["19", "13", "9"]
challenges = []
games = []
players = []


@client.event
async def on_ready():
    print(f"log in successful ({client.user})")


@client.event
async def on_message(message):
    global commands, boardSizes, challenges

    if ("hi bot-chan" in message.content.lower()):
        await client.send_message(message.channel, "hi!")

    if (message.content.lower().split(" ")[0] in commands and not message.author.bot):
        command = message.content.lower().split(" ")[0]
        contents = message.content.lower().split(" ")[1:]

        #check for contents of invalid length (maximum is two, with 'challenge' and 'stats')
        if (len(contents) in [1, 2]):
            if  ((len(contents) == 2 and command not in (commands[1], commands[8])) or (len(contents) == 1 and command == commands[1])):
                await client.send_message(message.channel, f"Ummm, no habla wrong command!")
                return 0
        elif command == "gohelp":
            await client.send_message(message.channel, embed = HELP_MESSAGE)
            return 0
        elif command == "gorules":
            await client.send_file(message.channel, "assets/rules_1.png")
            await client.send_file(message.channel, "assets/rules_2.png")
            return 0
        elif command == "kohelp":
            await client.send_message(message.channel, f"Positions are not allowed to repeat 2 times in a row. For more information see: https://senseis.xmp.net/?Ko")
            return 0
        else:
            await client.send_message(message.channel, f"Ummm, no habla wrong command!")
            return 0

        if (command == "accept" or command == "decline"):
            if (not in_game(message.author.id)):
                if (len(message.raw_mentions) != 1):
                    await client.send_message(message.channel, f"You have to mention the person that challenged you!")
                else:
                    exists = False

                    for board in boardSizes:
                        challenge = Challenge(message.raw_mentions[0], message.author.id, int(board))
                        for i in challenges:
                            if (i.challenger == challenge.challenger and i.challenged == challenge.challenged and i.boardSize == challenge.boardSize):
                                exists = True

                                if (command == commands[0]):
                                    if (not in_game(message.raw_mentions[0])):
                                        challenges = [x for x in challenges if x != i] #remove challenge from challenges
                                        acceptedGame = make_game(challenge)
                                        await client.send_message(message.channel, f"Challenge accepted!")
                                        imageData = acceptedGame.draw_goban()
                                        await client.send_file(message.channel, fp = imageData, filename = "goban.png")
                                    else: await client.send_message(message.channel, f"They're already in a game, try again later!")
                                else:
                                    challenges = [x for x in challenges if x != i] #remove challenge from challenges
                                    await client.send_message(message.channel, f"Challenge declined!")
                    if (not exists): await client.send_message(message.channel, f"No such challenge exists!")
            else: await client.send_message(message.channel, f"You're already in a game, you can't respond to challenges at this moment!")
        #challenge @user board
        elif (command == "challenge"):
            contents[1] = contents[1].split("x")[0] #try to change "_x_" to "_"

            if (message.author.mention == contents[0]):
                await client.send_message(message.channel, f"You can't challenge yourself!")
            elif (len(message.raw_mentions) != 1):
                await client.send_message(message.channel, f"You have to mention the person you want to challenge!")
            elif (contents[1] not in boardSizes):
                contents[1] = contents[1].split("x")[0]
                await client.send_message(message.channel, f"Oh no... you entered an invalid board size!")
            else:
                exists = False
                challenge = Challenge(message.author.id, message.raw_mentions[0], int(contents[1]))

                for i in challenges:
                    if (i.challenger == challenge.challenger and i.challenged == challenge.challenged):
                        exists = True
                    elif (i.challenger == challenge.challenged and i.challenged == challenge.challenger):
                        exists = True

                if (exists):
                    await client.send_message(message.channel, f"Challenge between those two players already exists!")
                else:
                    challenges.append(challenge.__copy__())
                    await client.send_message(message.channel, f"Challenge sent!")
        elif (command == "move"):
            inGame = False

            for player in players:
                if (player.id == message.author.id):
                    if (player.currentGame != False):
                        inGame = True
                        playerIndex = players.index(player)
                    break

            if inGame:
                currentGame = players[playerIndex].currentGame

                if (currentGame.blackPlayer.id == message.author.id and currentGame.blackToMove):
                      if (currentGame.make_move(contents[0]) == -1):
                          await client.send_message(message.channel, f"Illegal move!")
                      elif (currentGame.make_move(contents[0]) == -2):
                          await client.send_message(message.channel, f"Illegal move! (ko rule)")
                elif (currentGame.whitePlayer.id == message.author.id and not currentGame.blackToMove):
                      if (currentGame.make_move(contents[0]) == -1):
                          await client.send_message(message.channel, f"Illegal move!")
                      elif (currentGame.make_move(contents[0]) == -2):
                          await client.send_message(message.channel, f"Illegal move! (ko rule)")
                else:
                    await client.send_message(message.channel, f"It's not your move!")
                if (currentGame.winner):
                    if (currentGame.blackScore-currentGame.whiteScore != 0):
                        await client.send_message(message.channel, f"<@!{currentGame.winner.id}> won by {abs(currentGame.blackScore - currentGame.whiteScore)} points!")
                    else: 
                        await client.send_message(message.channel, f"<@!{currentGame.winner.id}> won by resignation!")

                    # Log game into stat storage
                    if currentGame.winner == currentGame.blackPlayer:
                        stats.log_game(currentGame.blackPlayer.id, currentGame.whitePlayer.id)
                    elif currentGame.winner == currentGame.whitePlayer:
                        stats.log_game(currentGame.whitePlayer.id, currentGame.blackPlayer.id)

                imageData = currentGame.draw_goban()
                await client.send_file(message.channel, fp = imageData, filename = "goban.png")
            else: await client.send_message(message.channel, f"You're not in a game!")
        elif (command == "withdraw"):
            exists = False

            for board in boardSizes:
                challenge = Challenge(message.author.id, message.raw_mentions[0], int(board))

                for i in challenges:
                    if (i.challenger == challenge.challenger and i.challenged == challenge.challenged and i.boardSize == challenge.boardSize):
                        exists = True
                        challenges = [x for x in challenges if x != i] #remove challenge from challenges
                        await client.send_message(message.channel, f"Challenge withdrawn!")

            if (not exists): await client.send_message(message.channel, f"Challenge doesn't exist!")
        elif (command == "stats"):
            if (len(message.raw_mentions) in [1, 2]):
                if   len(message.raw_mentions) == 1:
                    _playerID = message.raw_mentions[0]
                    _won, _lost, _played = stats.wins(_playerID), stats.losses(_playerID), stats.games_played(_playerID)
                elif len(message.raw_mentions) == 2:
                    _playerIDs = (message.raw_mentions[0], message.raw_mentions[1])
                    _stats_vs = stats.stats_vs(_playerIDs[0], _playerIDs[1])
                    _won, _lost, _played = _stats_vs[0], _stats_vs[1], _stats_vs[0]+_stats_vs[1] #won/lost from p1 perspective
                await client.send_message(message.channel, f"W{_won} L{_lost} P{_played}")
            else: await client.send_message(message.channel, f"Ummm, no habla wrong command!!")
def in_game(playerID):
    for player in players:
        if (player.id == playerID):
            if (player.currentGame): return True
    return False


def make_game(challenge):
    game = Game(challenge)
    games.append(game)
    firstExists = False
    secondExists = False

    for player in players:
        if (player.id == challenge.challenger):
            firstExists = True
            player.set_currentGame(game)
            game.set_players(player, False)
        if (player.id == challenge.challenged):
            secondExists = True
            player.set_currentGame(game)
            game.set_players(False, player)

    if not firstExists:
        players.append(Player(challenge.challenger, game))
        game.set_players(players[-1], False)
    if not secondExists:
        players.append(Player(challenge.challenged, game))
        game.set_players(False, players[-1])
    return game


tokenFile = open("token", "r")
token = tokenFile.read().strip()
tokenFile.close()
client.run(token)
