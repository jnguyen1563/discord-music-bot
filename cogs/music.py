import asyncio
import discord
from discord.ext import commands
from discord.utils import get
import youtube_dl

import os
import random
from youtubesearchpython.__future__ import VideosSearch

# Options for youtube-dl
ydl_opts = {
    'format': 'bestaudio/best',
    'noplaylist': 'True',
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
        self.loop = False
        self.queue = [] # Stored in (title,url) pairs
        self.search_results = None

########## Bot Join/Leave ##########

    @commands.command(aliases=['j'])
    async def join(self, ctx):
        '''
        Prompts the bot to join a voice channel
        It will join the channel of the user invoking the command
        '''

        # Attempt to get the channel that the message author is in
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            print('No user in voice channel')
            await ctx.send('No user in voice channel')
            return

        # Get the voice clients the bot is currently connected to
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

        # If already connected, move to channel where requested
        if self.voice and self.voice.is_connected():
            await self.voice.move_to(channel)
        # Otherwise connect to requested channel
        else:
            self.voice = await channel.connect()
            print(f'Bot has connected to {channel}')

        await ctx.send(f'Joined **{channel}**')

    @commands.command(aliases=['l'])
    async def leave(self, ctx):
        '''
        Prompts the bot to leave the voice channel
        Will only work if the user is in the same voice channel
        '''

        # Attempt to get the channel that the message author is in
        try:
            channel = ctx.message.author.voice.channel
        except AttributeError:
            print('No user in voice channel')
            await ctx.send('No user in voice channel')
            return

        # Get voice clients the bot is currently connected to
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

        # If connected, disconnect
        if self.voice and self.voice.is_connected():
            await self.voice.disconnect()
            print(f'Bot has left {channel}')
            await ctx.send(f'Left **{channel}**')
        else:
            print('Not in a voice channel')
            await ctx.send('Not in a voice channel')

########## Song Playing/Queue ##########

    async def add_to_queue(self, ctx, url: str):
        '''
        Helper function to add a song to the queue
        '''
        # Download video information and extract the title
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading video information')
            info_dict = ydl.extract_info(url, download=False)
            title = info_dict['title']

        # Add the video to the queue with (title, url) pairs
        self.queue.append((title, url))
        print(f'{title} added to queue (Position {len(self.queue)})')
        await ctx.send(f'***{title}*** added to queue **(Position {len(self.queue)}**)')


    @commands.command(aliases=['q', 'show', 'queue'])
    async def showqueue(self, ctx):
        '''
        Prompts the bot to show the current queue of songs
        '''
        # Checks to see if the queue is empty
        if not self.queue:
            print('Attempted to retrieve queue, but it is empty')
            await ctx.send('The queue is currently empty')
            return

        # Creates embed for song list
        queue_embed = discord.Embed(
            title='Current song queue',
            color=discord.Color.blurple()
        )

        # Creates the string containing queue information
        embed_message = ""
        if len(self.queue) > 10:
            # If the queue is greater than 10 songs, limits to 10 and prints how many remaining
            for index in range(10):
                embed_message += f'{index+1}: {self.queue[index][0]}\n'
            embed_message += f'*... and {len(self.queue) - 10} more*'
        else:
            # Prints every song to the queue
            for position, song in enumerate(self.queue):
                embed_message += f'{position+1}: {song[0]}\n'

        queue_embed.add_field(name='Song list', value=embed_message)
        # Sends the song queue as an embed
        await ctx.send(embed=queue_embed)

    @commands.command(aliases=['remove'])
    async def removequeue(self, ctx, index):
        '''
        Removes a song from the queue given its position
        '''
        index = int(index)
        await ctx.send(f'Removed ***{self.queue[index-1][0]}***')
        del self.queue[index-1]

    @commands.command(aliases=['clear'])
    async def clearqueue(self, ctx):
        '''
        Empties the song queue
        '''
        self.queue.clear()
        await ctx.send('Queue has been cleared')

    @commands.command()
    async def shuffle(self, ctx):
        '''
        Shuffles the entire queue
        '''
        random.shuffle(self.queue)
        await ctx.send('Shuffled the queue')

    async def song_is_playing(self, ctx):
        '''
        Helper function that returns whether or not a song is currently playing or paused
        '''
        if self.voice and (self.voice.is_playing() or self.voice.is_paused()):
            return True
        else:
            return False

    async def remove_old_song(self, ctx):
        '''
        Removes the old song.mp3 from the filesystem if possible
        '''
        try:
            if os.path.isfile('song.mp3'):
                os.remove('song.mp3')
                print('Removed old song')
        except PermissionError:
            print('Unable to remove old song')
            return

    def play_next_song(self, ctx, old_song=None):
        '''
        Closes out the last played song and moves onto the next song in the queue
        '''
        if self.loop:
            self.voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: self.play_next_song(ctx, old_song))
            self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
            self.voice.source.volume = 0.12
        else:
            # If moving on from a completed song, confirm finish
            if old_song:
                asyncio.run_coroutine_threadsafe(ctx.send(f'Finished playing *{old_song}*'), self.bot.loop)

            if self.queue:
                # Remove the next song on the list from the queue and play it
                next_song = self.queue.pop(0)
                asyncio.run_coroutine_threadsafe(self.play(ctx, next_song[1]), self.bot.loop)
            else:
                # Display a message once the end of the queue has been reached
                print('Reached end of queue')
                activity = discord.Game(name='nothing at the moment')
                asyncio.run_coroutine_threadsafe(self.bot.change_presence(status=discord.Status.idle, activity=activity), self.bot.loop)
                asyncio.run_coroutine_threadsafe(ctx.send('Reached end of queue'), self.bot.loop)


    @commands.command(aliases=['p'])
    async def play(self, ctx, url: str):
        '''
        Prompts the bot to play a song given a youtube url
        Will save the audio of the video as 'song.mp3'
        '''
        # Get voice clients bot is currently connected to
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

        # If there's already a song a playing or paused, put the new song in queue
        if await self.song_is_playing(ctx):
            await self.add_to_queue(ctx, url)
            return
        else:
            # Removes the previous song
            await self.remove_old_song(ctx)

        # Confirm audio setup
        await ctx.send('**Prepping the sax**')

        # Download audio from youtube video with previously set ydl options
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            print('Downloading audio')
            song_info = ydl.extract_info(url, download=True)
        
        # Search for downloaded audio file and rename it
        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                print(f'Renamed file: {file}')
                os.rename(file, 'song.mp3')

        # Print the current file being played
        display_name = song_info['title']
        await ctx.send(f'Playing: ***{display_name}***')
        activity = discord.Game(name=display_name)
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        print('Playing\n')

        # Play the audio
        self.voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: self.play_next_song(ctx, display_name))
        self.voice.source = discord.PCMVolumeTransformer(self.voice.source)
        self.voice.source.volume = 0.12

########## Playlists ##########

    @commands.command()
    async def playlist(self, ctx, url:str):
        '''
        Takes in a playlist and adds all its entries to queue
        '''

        with youtube_dl.YoutubeDL({'quiet': 'True', 'ignoreerrors': 'True'}) as ydl:
            print('Downloading playlist info')
            await ctx.send('Downloading playlist info')
            playlist_info = ydl.extract_info(url, download=False)

        playlist_queue = []    
        for song in playlist_info['entries']:
            if not song:
                continue
            playlist_queue.append((song['title'], song['webpage_url']))

        self.queue += playlist_queue

        if not await self.song_is_playing(ctx):
            self.play_next_song(ctx)

########## Search ##########

    @commands.command()
    async def search(self, ctx, *, search_terms:str):
        '''
        Searches youtube for its first three results for search terms
        '''
        try:
            # Search with search terms
            video_search = VideosSearch(search_terms, limit=3)
            video_results = await video_search.next()
        except:
            print('Could not complete search')
            await ctx.send('Invalid search')
            return

        # Store search results
        self.search_results = video_results['result']

        # Initialize embed for search results
        search_embed = discord.Embed(
            title='Search Results',
            description=f'for "{search_terms}"',
            color=discord.Color.blurple()
        )

        for index, video in enumerate(video_results['result']):
            search_embed.add_field(name=f'{index+1}. {video["title"]}', value=f'{video["channel"]["name"]} - {video["duration"]} - {video["viewCount"]["text"]}')

        await ctx.send(embed=search_embed)

    @commands.command()
    async def playsearch(self, ctx, position):
        '''
        Picks a video from search results and adds it to queue 
        '''
        # Error if no search has been done yet
        if not self.search_results:
            await ctx.send('No search results found, use the >search command first')
            return

        # Choose the selected video from position
        try:
            selected_video = self.search_results[int(position)-1]
            self.search_results.clear()
        except:
            await ctx.send('Invalid position number')
            print('Tried to access search, but invalid index was given')
            return
        
        # Play the selected video
        await self.play(ctx, selected_video['link'])

########## Media controls ##########

    @commands.command(aliases=['pa'])
    async def pause(self, ctx):
        '''
        Prompts the bot to pause the current song
        Will return a message if there is no song loaded
        '''
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

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
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

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

    @commands.command(aliases=['s', 'skip'])
    async def stop(self, ctx):
        '''
        Prompts the bot to stop and remove the current song
        '''
        self.voice = get(self.bot.voice_clients, guild=ctx.guild)

        # Check if music is playing and stop it
        if await self.song_is_playing(ctx):
            print('Song skipped')
            self.voice.stop()
            await ctx.send('Song skipped')
        else:
            print('Tried to stop, but no music playing')
            await ctx.send('No music playing')

    @commands.command()
    async def loop(self, ctx):
        '''
        Toggles loop mode, which causes the bot to loop the currently playing song
        '''
        if self.loop:
            await ctx.send('No longer looping')
            self.loop = False
        else:
            await ctx.send('Looping current song')
            self.loop = True

def setup(bot):
    bot.add_cog(Music(bot))
    print('Music extension is loaded')