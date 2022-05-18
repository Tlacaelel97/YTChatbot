import discord 
from discord.ext import commands

#initialize bot
client = commands.Bot(command_prefix = '!')

@client.event

async def on_ready():
    print('The bot is now ready for use!')
    print('-'*70)

@client.command()
async def hello(ctx):
    await ctx.send("Hello, I am the youtube bot")

client.run('OTc2MzI2NDc3MzE2NTIyMDc0.Gj9FYQ.IGjwic4WdU8ga7xiREeQKfmGjw7vunZ-vbZpr4') 

