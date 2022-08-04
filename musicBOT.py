import discord
from discord.ext import commands
import youtube_dl
from secrets import botToken

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix = '!', intents = intents)

@client.event
async def on_ready():
  print("Bot is ready")

# Start the music
@client.command(pass_context = True)
async def start(ctx, url):  
  if (ctx.author.voice):
    channel = ctx.message.author.voice.channel
    await channel.connect()
  else:
    await ctx.send("You are not in a voice channel!")

  ctx.voice_client.stop()
  FFMPEG_OPTIONS = {'options': '-vn'}
  YDL_OPTIONS = {'format': 'bestaudio'}
  
  voice_client = ctx.voice_client

  with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
    info = ydl.extract_info(url, download=False)
    url2 = info['formats'][0]['url']
    source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
    voice_client.play(source)

    print("Playing")

# Resume the music
@client.command(pass_context = True)
async def resume(ctx):
  ctx.voice_client.resume()
  await ctx.send("Resumed")

# Pause the music 
@client.command(pass_context = True)
async def pause(ctx):
  ctx.voice_client.pause()
  await ctx.send("Paused")

# Disconnect the bot
@client.command(pass_context = True)
async def leave(ctx):
  if (ctx.voice_client):
    await ctx.guild.voice_client.disconnect()
    await ctx.send("I left the voice channel")
  else:
    await ctx.send("I am not in a voice channel :(")

client.run(botToken)