import discord
from discord.ext import commands

import json

# load in config file
with open('config.json', 'r') as f:
    config = json.load(f)

# bot info
TOKEN = config['token']
bot = commands.Bot(command_prefix='>', help_command=None)

@bot.event
async def on_ready():
    activity = discord.Game(name='nothing at the moment')
    await bot.change_presence(status=discord.Status.idle, activity=activity)
    print('Ready to play music')

load_order = ['loading', 'help', 'music']
for extension in load_order:
    try:
        bot.load_extension(f'cogs.{extension}')
    except Exception as e:
        print(f'Failed to load extension: {extension}')


bot.run(TOKEN)