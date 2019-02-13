#id 545306487191240704
#token NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8
#perm 523328

import discord
from game import Game

client = discord.Client()
commands = ["accept", "challenge", "decline", "move"]
boardSizes = ["19", "13", "9"]
challenges = []

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

        if (command == commands[0] or command == commands[2]):
            if (len(message.raw_mentions) != 1):
                await client.send_message(message.channel, f"You have to mention the person that challenged you!")
            else:
                exists = False
                for board in boardSizes:
                    challengeID = board+str(int(message.raw_mentions[0])+int(message.author.id))
                    if ([message.raw_mentions[0], challengeID] in challenges):
                        exists = True
                        challenges = [x for x in challenges if x != [message.raw_mentions[0], challengeID]] #remove challengeID from challenges
                        if (command == commands[0]):
                            make_game(challengeID)
                            await client.send_message(message.channel, f"Challenge accepted!")
                        else:
                            await client.send_message(message.channel, f"Challenge declined!")
                if (not exists): await client.send_message(message.channel, f"No such challenge exists!")

        #challenge @user board
        if (command == commands[1]):
            contents[1] = contents[1].split("x")[0] #try to change "_x_" to "_"
            if (message.author.mention == contents[0]):
                await client.send_message(message.channel, f"You can't challenge yourself!")
            elif (len(message.raw_mentions) != 1):
                await client.send_message(message.channel, f"You have to mention the person you want to challenge!")
            elif (contents[1] not in boardSizes):
                contents[1] = contents[1].split("x")[0]
                await client.send_message(message.channel, f"Oh no... you entered an invalid board size!")
            else:
                challengeID = contents[1]+str(int(message.raw_mentions[0])+int(message.author.id))
                if ([message.author.id, challengeID] not in challenges and [message.raw_mentions[0], challengeID] not in challenges): 
                    challenges.append([message.author.id, challengeID])
                    await client.send_message(message.channel, f"Challenge sent!")
                else:
                    await client.send_message(message.channel, f"Challenge between those two players already exists!")

        if (command == commands[3]):
            pass
def make_game(challengeID):
    return 0

client.run("NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8")
