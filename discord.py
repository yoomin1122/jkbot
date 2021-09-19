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

bot = commands.Bot(command_prefix=',')


@bot.event
async def on_ready():
    status = cycle(["노래하는재깨봇", ",명령어"])

    @tasks.loop(seconds=10)
    async def change_status():
        await bot.change_presence(activity=discord.Game(next(status)))

    change_status.start()


@bot.command()
async def 핑(ctx):
    await ctx.send(embed=discord.Embed(title=f'퐁! {round(round(bot.latency, 4) * 1000)}ms', color=0x2eaf))


@bot.command()
async def 유튜브(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://youtube.com/results?' + query_string

    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.send('https://youtube.com/watch?v=' + search_results[0])


@bot.command()
async def 따라해(ctx, *, text):
    await ctx.send(text)


@bot.command()
async def 청소(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

    await ctx.send(embed=discord.Embed(title="메시지 삭제 알림",
                                       description="최근 디스코드 채팅 {}개가\n관리자 {}님의 요청으로 인해 정상 삭제 조치 되었습니다".format(amount,
                                                                                                             ctx.author),
                                       color=0x2eaf))


@bot.command()
async def 명령어(ctx):
    await ctx.send(
        embed=discord.Embed(title=f'명령어', description=f'http://commands.jkbot.kro.kr 여기 확인해줘!', color=0x2eaf))


@bot.command()
async def 뽑기(ctx):
    ran = randint(1, 9)
    await ctx.send(embed=discord.Embed(title=f'뽑기에서 {ran}이(가) 나왔습니다.', color=0x2eaf))


bot.run(TOKEN)
