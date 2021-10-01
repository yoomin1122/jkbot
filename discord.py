import discord
from discord.ext import commands, tasks
from discord.utils import get
import asyncio
import time
from random import *
from itertools import cycle
import urllib.parse, urllib.request, re
from webserver import keep_alive
import os
import datetime
from discord.ext.commands import CommandNotFound
from googleapiclient.discovery import build

bot = commands.Bot(command_prefix=',')
api_key = "AIzaSyBlucQspEhQWPSMr378mg63d8SK_FyMgCI"
bot.remove_command("help")


@bot.event
async def on_ready():
    status = cycle(["https://jkbot.xyz", ",명령어"])

    @tasks.loop(seconds=5)
    async def change_status():
        await bot.change_presence(activity=discord.Game(next(status)))

    change_status.start()


@bot.command()
async def 핑(ctx):
    await ctx.send(embed=discord.Embed(title=f':ping_pong: 퐁! {round(round(bot.latency, 4) * 1000)}ms', color=0xb5fb94))


@bot.command(aliases=["help", "도움", "commands"])
async def 명령어(ctx):
    embed = discord.Embed(color=0xb5fb94)
    embed.set_author(name="명령어", icon_url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name=":point_right: 접두사", value="접두사는 ,(쉼표) 입니다.", inline=False)
    embed.add_field(name=":loudspeaker: 서버관리", value="청소", inline=False)
    embed.add_field(name=":video_game: 놀이", value=f"따라해, 뽑기", inline=False)
    embed.add_field(name=":mag_right: 검색", value=f"유튜브, 구글(이미지)", inline=False)
    embed.add_field(name=":desktop: 재깨봇 공식 사이트", value="https://jkbot.xyz", inline=False)
    await ctx.send(embed=embed)


@bot.command(aliases=["youtube", "유튭"])
async def 유튜브(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://youtube.com/results?' + query_string

    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send('https://youtube.com/watch?v=' + search_results[0])

#hellothisisverification

@bot.command()
async def hellothisisverification(ctx, *, text):
    await ctx.message.delete()
    await ctx.send("⅄ooWıu#5973")



@bot.command()
async def 따라해(ctx, *, text):
    await ctx.message.delete()
    await ctx.send(text)


@bot.command()
async def 뽑기(ctx):
    ran = randint(1, 9)
    await ctx.send(embed=discord.Embed(title=f'뽑기에서 {ran}이(가) 나왔습니다.', color=0xb5fb94))


@bot.command()
async def 청소(ctx, number:int=None):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.send('숫자를 입력해주세요.')
                elif 100 < number:
                    await ctx.message.delete()
                    await ctx.send(f'{ctx.message.author.mention} 100보다 큰 수는 입력할 수 없습니다.', delete_after=5)
                else:
                    deleted = await ctx.message.channel.purge(limit=number)
                    await ctx.send(f'{ctx.message.author.mention}에 의해 {len(deleted)}개의 메세지가 삭제되었습니다.')
            except:
              await ctx.send("삭제가 불가합니다.")
        else:
          await ctx.send('이 명령을 사용할 수 있는 권한이 없습니다.')
    else:
      await ctx.send('DM에선 불가합니다.')


@bot.command(aliases=["info", "정보"])
async def 내정보(ctx):
    user = ctx.author
    date = datetime.datetime.utcfromtimestamp(((int(user.id) >> 22) + 1420070400000) / 1000)
    embed = discord.Embed(color=0xb5fb94)
    embed.set_author(name="아래에서 내 정보를 확인하세요!", icon_url="")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name="이름", value=ctx.author.name, inline=False)
    embed.add_field(name="생일", value=f"{date.year}년 {date.month}월 {date.day}일", inline=False)
    embed.add_field(name="아이디", value=f"{user.id}", inline=False)
    await ctx.reply(embed=embed, mention_author=False)


@bot.command(aliases=["botinfo", "재깨봇"])
async def 봇정보(ctx):
    embed = discord.Embed(color=0xb5fb94)
    embed.set_author(name="재깨봇 정보", icon_url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.set_thumbnail(url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.add_field(name="개발자", value="유민#5973", inline=False)
    embed.add_field(name="생일", value=f"2021년 5월 28일", inline=False)
    embed.add_field(name="사이트", value=f"https://jkbot.xyz", inline=False)
    await ctx.reply(embed=embed, mention_author=False)


@bot.command(aliases=["show"])
async def 구글(ctx, *, search):
    ran = randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="f10853740d3d5e759", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"`{search}`을(를) 검색했을때 결과입니다.", color=0xb5fb94)
    embed1.set_image(url=url)
    await ctx.send(embed=embed1)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      em = discord.Embed(title=f"명령어를 찾을수 없습니다!", color=0xb5fb94) 
      await ctx.send(embed=em)
      return
    raise error


bot.run(TOKEN)
