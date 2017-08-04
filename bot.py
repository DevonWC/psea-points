# -*- coding: cp1252 -*-
import discord, asyncio, logging, math

import settings
from commands import psea, commandCall

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

with open('token.txt', 'r') as f:
    token = f.read().strip("\n")

client = discord.Client()


@client.event
@asyncio.coroutine
def on_ready():
    print("bot está online como", client.user.name)

@client.event
@asyncio.coroutine
def on_message(message):

    if not message.author.bot and message.channel.id not in settings.forbiddenChannels:

        messagelower = message.content.lower()

        #Checks for a command
        if message.content.startswith(settings.operator):

            yield from client.delete_message(message)

            isMod = False

            for role in message.author.roles:
                if role.id in settings.modRoles:
                    isMod = True

            if isMod:
                command = message.content.lower().lstrip(settings.operator).split()
 
                if command[0].split()[0] == commandCall.psea.call:
                    try:
                        if len(command) == 1:
                            botTalk = yield from client.send_message(message.channel, psea.fetchPointList())
                            print(command)

                        if len(command) == 2:
                            botTalk = yield from client.send_message(message.channel, "[{0}: {1}]".format(message.mentions[0].name, psea.getUserPoints(int(message.mentions[0].id))))
                            print(message.mentions[0].name, command)

                        if len(command) > 2 and int(command[2]) > 0: 
                            psea.addPoints(int(message.mentions[0].id), message.mentions[0].name, int(command[2]), False)
                            print(command)
                            botTalk = yield from client.send_message(message.channel, "Adicionado {0} ponto(s) para ".format(command[2]) + message.mentions[0].name)

                        elif len(command) > 2 and type(int(command[2][1:])):
                            psea.addPoints(int(message.mentions[0].id), message.mentions[0].name, command[2], True)
                            botTalk = yield from client.send_message(message.channel, "Removido {0} ponto(s) de ".format(command[2][1:]) + message.mentions[0].name)                        
                            print(command)

                       
                        yield from asyncio.sleep(10); yield from client.delete_message(botTalk)

                    except Exception as e:
                        print(e)               

#-------------------------------
client.run(token)
