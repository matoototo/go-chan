#id 545306487191240704
#token NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8
#perm 523328

import discord
from game import Game

client = discord.Client()
commands = ["accept", "challenge", "decline", "move"]
challenges = []

@client.event
async def on_ready():
    print(f"log in successful ({client.user})")

@client.event
async def on_message(message):
    if ("hi bot-chan" in message.content.lower()):
        await client.send_message(message.channel, "hi!")

    if (message.content.lower().split(" ")[0] in commands):
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

        if (command == commands[0]):
            pass
        if (command == commands[1]):
            if (message.author.mention == contents[0]):
                await client.send_message(message.channel, f"You can't challenge yourself!")

        if (command == commands[2]):
            pass
        if (command == commands[3]):
            pass


client.run("NTQ1MzA2NDg3MTkxMjQwNzA0.D0Xv8w.e7L44QaHK6ndZigjkSTWGchrEZ8")
