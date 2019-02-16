#id 545306487191240704
#token NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8
#perm 523328

import discord
from game import Game, Challenge
from player import Player

client = discord.Client()
commands = ["accept", "challenge", "decline", "move"]
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

        #check for contents of invalid length (maximum is two, with 'challenge')
        if (len(contents) in [1, 2]):
            if  ((len(contents) == 2 and command != commands[1]) or (len(contents) == 1 and command == commands[1])):
                await client.send_message(message.channel, f"Ummm, no habla wrong command!")
                return 0
        else:
            await client.send_message(message.channel, f"Ummm, no habla wrong command!")
            return 0

        if (command == "accept" or command == "decline"):
            if (len(message.raw_mentions) != 1):
                await client.send_message(message.channel, f"You have to mention the person that challenged you!")
            else:
                exists = False
                for board in boardSizes:
                    challenge = Challenge(message.raw_mentions[0], message.author.id, int(board))
                    for i in challenges:
                        if (i.challenger == challenge.challenger and i.challenged == challenge.challenged and i.boardSize == challenge.boardSize):
                            exists = True
                            challenges = [x for x in challenges if x != i] #remove challenge from challenges
                            if (command == commands[0]):
                                make_game(challenge)
                                await client.send_message(message.channel, f"Challenge accepted!")
                            else:
                                await client.send_message(message.channel, f"Challenge declined!")
                if (not exists): await client.send_message(message.channel, f"No such challenge exists!")

        #challenge @user board
        if (command == "challenge"):
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
                challenge = Challenge(message.author.id, message.raw_mentions[0], contents[1])
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
                
        if (command == "move"):
            pass

def make_game(challenge):
    game = Game(challenge)
    games.append(game)
    firstExists = False
    secondExists = False
    for player in players:
        if (player.id == challenge.challenger):
            firstExists = True
            player.set_currentGame(game)
        if (player.id == challenge.challenged):
            secondExists = True
            player.set_currentGame(game)
    if not firstExists: players.append(Player(challenge.challenger, game))
    if not secondExists: players.append(Player(challenge.challenged, game))
    #should send blank board
    return 0

client.run("NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8")
