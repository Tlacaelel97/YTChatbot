import discord 
from discord.ext import commands
from discord import FFmpegPCMAudio
import requests
import json

#import Bot token

from apikeys import *

intents = discord.Intents.default()
intents.members=True

queues = {}

def check_queue(ctx,id):
    if queues[id] != []:
        voice = ctx.guild.voice_client
        #remove the first element
        source = queues[id].pop(0)
        player = voice.play(source)

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
Goodbye to a member
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
        voice = await channel.connect()
        source = FFmpegPCMAudio('ambient-bell-guitar.wav')
        player = voice.play(source)

    else:
        await ctx.send('You must be in a voice channel to run this command')

@client.command(pass_context= True)
async def leave(ctx):
    #If the bot is in a voiice channel
    if (ctx .voice_client):
        #Then leave the channel
        await ctx.guild.voice_client.disconnect()
        #Say goodbye
        await ctx.send('I have left the voice channel')
    else:
        await ctx.send('I am not in a voice channel')

"""
Pause, resume, stop
"""
@client.command(pass_context=True)
async def pause(ctx):
    #get channel voice
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    #if bot is playing
    if voice.is_playing():
        voice.pause
    #it it doesn't playing
    else:
        await ctx.send('At the moment, there is no audio playing in the voice channel')

@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    #If th emusic is paused
    if voice.is_paused():
        #play
        voice.resume()
    # it it´s not paused
    else:
        await ctx.send('At the moment, there is no song paused!')

@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()

@client.command(pass_context=True)
async def play(ctx,arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    #check if there is another song in the list
    player = voice.play(source,after=lambda x=None: check_queue(ctx,ctx.message.guild.id))

@client.command(pass_context=True)
async def queue(ctx,arg):
    voice = ctx.guild.voice_client
    song = arg + '.wav'
    source = FFmpegPCMAudio(song)
    #get id of the discord server
    guild_id = ctx.message.guild.id
    if guild_id in queues:
        queues[guild_id].append(source)

    else:
        queues[guild_id] = [source]

    await ctx.send('Added to queue')



client.run(BOTTOKEN) 

