import discord
from discord.ext import commands

class Help(commands.Cog, name='Help'):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        '''
        Custom help command
        '''
        # Initialize the embed
        help_embed = discord.Embed(
        title='List of Commands',
        color=discord.Color.blurple()
        )   

        # Command names
        help_embed.add_field(name='Command Name', value=(
            """**Voice Channel Controls**
            join
            leave
            **Media Controls**
            play <url>
            pause
            resume
            stop
            loop
            **Queue Controls**
            queue
            clearq
            removeq <#>
            shuffle
            **Playlist**
            playlist <url>
            **Search**
            search <words>
            playsearch <#>"""), inline=True)
        
        # Command descriptions
        help_embed.add_field(name='Description', value=(
            """ ----------------------------------------
            Bot joins voice channel user is in
            Bot leaves voice channel user is in
            ----------------------------------------
            Play song, adds to queue if song is already playing
            Pauses the current song
            Resumes current song if paused
            Ends the current song
            Sets the bot to loop the current song
            ----------------------------------------
            Shows the current list of songs in the queue
            Completely removes all songs from the queue
            Removes song from the queue at a given position
            Shuffles the entire queue
            ----------------------------------------
            Adds playlist entries into queue
            ----------------------------------------
            Searches for the top 3 search results on Youtube
            Plays the selected song from search results"""), inline=True)

        await ctx.send(embed=help_embed)

    @commands.command()
    async def banger(self, ctx, days=0):
        await ctx.send(f'Days without a banger: **{days}**')

    @commands.command()
    async def sax(self, ctx):
        await ctx.send("Big Band don't \"wadataaah\" to the \"shamaca\", 'cause that's a \"comacomalipachah\", dig?")

def setup(bot):
    bot.add_cog(Help(bot))
    print('Help extension is loaded')