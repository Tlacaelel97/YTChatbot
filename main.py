import discord 
from discord.ext import commands
import requests
import json

#import Bot token

from apikeys import *

intents = discord.Intents.default()
intents.members=True

#initialize bot
client = commands.Bot(command_prefix = '!',intents=intents)

@client.event

async def on_ready():
    print('The bot is now ready for use!')
    print('-'*70)

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the youtube bot")

@client.command()
async def goodbye(ctx):
    await ctx.send("Goodbye, have a nice day!")

"""
Welcome a New member
"""

@client.event
#when a user enter the server
async def on_member_join(member):

    jokeurl = "https://joke3.p.rapidapi.com/v1/joke"

    headers = {
        "X-RapidAPI-Host": JOKEAPI,
        "X-RapidAPI-Key": JOKETOKEN
    }

    response = requests.request("GET", jokeurl, headers=headers)

    #print(response.text)

    channel = client.get_channel(770542136160157740)
    await channel.send('Hello and welcome to the server! Here is a joke:')
    await channel.send(json.loads(response.text)['content'])

"""
Goodbye to a membr
"""
@client.event
async def on_member_remove(member):
    channel = client.get_channel(770542136160157740)
    await channel.send('Goodbye')

"""
Joining and leaving a channel voice
"""

@client.command(pass_context= True)
async def join(ctx):
    if (ctx.author.voice):
        channel = ctx.message.author.voice.channel
        await channel.connect()
    else:
        await ctx.send('You must be in a voice channel to run this command')

@client.command(pass_context= True)
async def leave(ctx):
    #If the bot is in a voiice channel
    if (ctx .voice_client):
        #Then leave the channel
        await ctx.guild.voice_client.disconnect()
        #Say goodbye
        await ctx.send('I left the voice channel')
    else:
        await ctx.send('I am not in a voice channel')

client.run(BOTTOKEN) 

