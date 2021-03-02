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

@bot.command(aliases=['h'])
async def help(ctx):
    # Initialize the embed
    help_embed = discord.Embed(
        title='List of Commands',
        color=discord.Color.blurple()
    )

    help_embed.add_field(name='Voice Channel', value="""join:          Bot joins voice channel user is in
                                                        leave:         Bot leaves voice channel user is in""", inline=False)
    help_embed.add_field(name='Media Controls', value="""play (url):    Play song, adds to queue if song is already playing
                                                         pause:         Pauses the current song
                                                         resume:        Resumes the current song if paused
                                                         stop:          Ends the current song
                                                         loop:          Sets the bot to loop the current song""", inline=False)
    help_embed.add_field(name='Queue Controls', value="""queue:         Shows the current list of songs in the queue
                                                         clearq:        Completely removes all songs from queue
                                                         removeq (pos): Removes song from queue at given position""", inline=False)

    await ctx.send(embed=help_embed)


load_order = ['loading', 'music']
for extension in load_order:
    try:
        bot.load_extension(f'cogs.{extension}')
    except Exception as e:
        print(f'Failed to load extension: {extension}')


bot.run(TOKEN)