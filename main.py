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

@client.event
async def on_member_remove(member):
    channel = client.get_channel(770542136160157740)
    await channel.send('Goodbye')

client.run(BOTTOKEN) 

