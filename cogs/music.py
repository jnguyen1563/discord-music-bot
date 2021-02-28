import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl
import os


# Options for youtube-dl
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],            
}

class Music(commands.Cog, name='Music'):
    
    def __init__(self, bot):
        self.bot = bot
        self.voice = None
        self.queue = {}

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        '''
        Prompts the bot to join a voice channel
        It will join the channel of the user invoking the command
        '''
        bot = self.bot

        # Attempt to get the channel that the message author is in
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            print('No user in voice channel')
            await ctx.send('No user in voice channel')
            return

        # Get the voice clients the bot is currently connected to
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # If already connected, move to channel where requested
        if self.voice and self.voice.is_connected():
            await self.voice.move_to(channel)
        # Otherwise connect to requested channel
        else:
            self.voice = await channel.connect()
            print(f'Bot has connected to {channel}')

        await ctx.send(f'Joined {channel}')

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        '''
        Prompts the bot to leave the voice channel
        Will only work if the user is in the same voice channel
        '''
        bot = self.bot

        # Attempt to get the channel that the message author is in
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            print('No user in voice channel')
            await ctx.send('No user in voice channel')
            return

        # Get voice clients the bot is currently connected to
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # If connected, disconnect
        if self.voice and self.voice.is_connected():
            await self.voice.disconnect()
            print(f'Bot has left {channel}')
            await ctx.send(f'Left {channel}')
        else:
            print('Not in a voice channel')
            await ctx.send('Not in a voice channel')

    @commands.command(aliases=['p'])
    async def play(self, ctx, url: str):
        '''
        Prompt the bot to play a song given a youtube url
        Will save the audio of the video as 'song.mp3'
        '''
        song_exists = os.path.isfile('song.mp3')
        bot = self.bot

        # Delete old song files
        try:
            if song_exists:
                os.remove('song.mp3')
                print('Removed old song')
        except PermissionError:
            print('Attempted to delete song, but currently being played')
            await ctx.send('Music is currently playing, stop the current song first')
            return

        # Get voice clients bot is currently connected to
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # Confirm audio setup
        await ctx.send('Prepping the saxophone')

        # Download audio from youtube video with previously set ydl options
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio')
            ydl.download([url])
        
        # Search for downloaded audio file and rename it
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                filename = file
                print(f'Renamed file: {file}\n')
                os.rename(file, 'song.mp3')

        # Play the audio
        self.voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{filename} has finished playing'))
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = 0.12

        # Print the current file being played
        display_name = filename[:-16]
        await ctx.send(f'Playing: {display_name}')
        print('Playing\n')

    @commands.command(aliases=['pa'])
    async def pause(self, ctx):
        '''
        Prompts the bot to pause the current song
        Will return a message if there is no song loaded
        '''
        bot = self.bot
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # Check that music is playing and pause it
        if self.voice and self.voice.is_playing():
            print('Music paused')
            self.voice.pause()
            await ctx.send('Music paused')
        else:
            print('Tried to pause, but no music playing')
            await ctx.send('No music playing')

    @commands.command(aliases=['r'])
    async def resume(self, ctx):
        '''
        Prompts the bot to resume the currently paused song
        Returns a message if the current song is already running or no song is loaded
        '''
        bot = self.bot
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # Check that music is paused and resume
        if self.voice and self.voice.is_paused():
            print('Music resumed')
            self.voice.resume()
            await ctx.send('Music resumed')
        elif self.voice and not self.voice.is_paused():
            print('Tried to resume, but music is already playing')
            await ctx.send('Current song is already playing')
        else:
            print('Tried to resume, but no song is playing')
            await ctx.send('No song to resume')

    @commands.command(aliases=['s'])
    async def stop(self, ctx):
        '''
        Prompts the bot to stop and remove the current song
        '''
        bot = self.bot
        self.voice = get(bot.voice_clients, guild=ctx.guild)

        # Check if music is playing and stop it
        if self.voice and (self.voice.is_playing() or self.voice.is_paused()):
            print('Music stopped')
            self.voice.stop()
            await ctx.send('Music stopped')
        else:
            print('Tried to stop, but no music playing')
            await ctx.send('No music playing')

def setup(bot):
    bot.add_cog(Music(bot))
    print('Music extension is loaded')