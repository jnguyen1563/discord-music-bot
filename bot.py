import discord
from discord.ext import commands

# bot info
TOKEN = 'NzUwMjI5MTU5MjQ2MTY4MTM1.X03fWg.LAHvnXM1xODajszAhAnU9gk6xB0'
bot = commands.Bot(command_prefix='>', help_command=None)

@bot.event
async def on_ready():
    activity = discord.Activity(name='to the good stuff', type=discord.ActivityType.listening)
    await bot.change_presence(status=discord.Status.online, activity=activity)
    print('Ready to play music')

load_order = ['loading', 'help', 'music']
for extension in load_order:
    try:
        bot.load_extension(f'cogs.{extension}')
    except Exception as e:
        print(f'Failed to load extension: {extension}')


bot.run(TOKEN)