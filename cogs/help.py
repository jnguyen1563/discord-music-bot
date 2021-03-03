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
            removeq <#>"""), inline=True)
        
        # Command descriptions
        help_embed.add_field(name='Description', value=(
            """ ----------------------------------------
            : Bot joins voice channel user is in
            : Bot leaves voice channel user is in
            ----------------------------------------
            : Play song, adds to queue if song is already playing
            : Pauses the current song
            : Resumes current song if paused
            : Ends the current song
            : Sets the bot to loop the current song
            ----------------------------------------
            : Shows the current list of songs in the queue
            : Completely removes all songs from the queue
            : Removes song from the queue at a given position"""), inline=True)

        await ctx.send(embed=help_embed)

def setup(bot):
    bot.add_cog(Help(bot))
    print('Help extension is loaded')