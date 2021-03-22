# Discord Music Bot

## Summary
Discord bot written with discord.py that can be used to play music into the voice chat.  
Uses a combination of ffmpeg and youtube-dl to download the mp3 files onto the host's device.  

The bot will NOT work unless ffmpeg is installed and added to the system PATH.  
You also need to make a config.json file that contains the bot token.  
To start the bot, go to the directory and type:  
```python bot.py```  

## Features
This bot currently supports:
- Playing music from youtube videos or soundcloud links
- Pause, stop, resume, loop commands
- Queuing multiple songs to be played in order
- Searching for youtube videos and playing directly from discord client
- Custom help command
- Reloading extensions directly in client

