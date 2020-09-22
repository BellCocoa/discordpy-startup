import discord
from discord.ext import commands

import os


bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

if not discord.opus.is_loaded():
    discord.opus.load_opus("heroku-buildpack-libopus")
    

@bot.command(aliases=["connect","summon"]) #connect or summonで呼び出しctx
async def join(ctx):
    """ボイスチャンネルに接続中"""
    voice_state = ctx.author.voice
    
    if (not voice_state) or (not voice_state.channel):
        await ctx.send("ボイスチャンネルに入ってから呼び出して下さい。")
        return
    
   channel = voice_state.channel

     await channel.connect()
     print("connected to:",channel.name)
        
        
 @bot.command(aliases=["disconnect","bye"])
async def leave(ctx):
    """チャンネルから切断しました。"""
    voice_client = ctx.message.guild.voice_client
    
    if not voice_client:
        await ctx.send("ボイスチャンネルに参加していません。")
        return
        
        
@bot.command(aliases=["test"])
async def play(ctx):
    """音声ファイルを流します。"""
    voice_client = ctx.message.guild.voice_client
    
    if not voice_client:
        await ctx.send("ボイスチャンネルに参加していません。")
        return
    
    if not ctx.message.attachments:
        await ctx.send("ファイルが添付されていません。")
        return
    
   await ctx.message.attachments[0].save("tmp.mp3")

   ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
   voice_client.play(ffmpeg_audio_source)

 await ctx.send("再生しました。")
    
bot.run(token)
