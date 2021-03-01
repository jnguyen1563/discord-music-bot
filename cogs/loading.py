import discord
from discord.ext import commands

class Loading(commands.Cog, name='Loading'):

    def __init__(self, bot):
        self.bot = bot

    # Loads extension
    @commands.command()
    async def load(self, ctx, extension):
        '''Loads in an extension
        '''
        self.bot.load_extension(f'cogs.{extension}')

    # Unloads extension
    @commands.command()
    async def unload(self, ctx, extension):
        '''Unloads an extension
        '''
        self.bot.unload_extension(f'cogs.{extension}')

    # Refreshes extension
    @commands.command()
    async def reload(self, ctx, extension):
        '''Reboots an extension
        '''
        self.bot.reload_extension(f'cogs.{extension}')

def setup(bot):
    bot.add_cog(Loading(bot))
    print('Loading extension is loaded')