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

intents = discord.Intents.default()
intents.members = True

client = commands.Bot(command_prefix=[",", "재깨야 "], intents=intents)
client.remove_command("help")
#pip install discord-py-slash-command
@client.event
async def on_ready():
    status = cycle(["https://jkbot.xyz", ",명령어"])

    @tasks.loop(seconds=5)
    async def change_status():
        await client.change_presence(activity=discord.Game(next(status)))

    change_status.start()


@client.command()
async def 핑(ctx):
    await ctx.send(embed=discord.Embed(title=f':ping_pong: 퐁! {round(round(client.latency, 4) * 1000)}ms', color=0xb5fb94))


@client.command(aliases=["멤버수"])
async def member_count(ctx):
  a=ctx.guild.member_count
  b=discord.Embed(title=f"{ctx.guild.name}(의)에 멤버수는",description=f"{a}명 입니다.",color=(0xb5fb94))
  await ctx.reply(embed=b, mention_author=False)


@client.command()
async def 서버정보(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)

    owner = str(ctx.guild.owner.id)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)

    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + "(의) 서버 정보", 
        color=0xb5fb94
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="서버 설명", value=description, inline=False)
    embed.add_field(name="서버장", value=f'<@{owner}>', inline=False)
    embed.add_field(name="서버 아이디", value=id, inline=False)
    embed.add_field(name="서버 위치", value=region, inline=False)
    embed.add_field(name="멤버수", value=memberCount, inline=False)

    await ctx.reply(embed=embed, mention_author=False)

@client.command(aliases=["help", "도움", "commands", "도움말"])
async def 명령어(ctx):
    embed = discord.Embed(color=0xb5fb94)
    embed.set_author(name="명령어", icon_url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.set_thumbnail(url=ctx.author.avatar_url)
    embed.add_field(name=":point_right: 접두사", value="접두사는 `,(쉼표)`와 `재깨야 `입니다", inline=False)
    embed.add_field(name=":loudspeaker: 서버관리", value="청소", inline=False)
    embed.add_field(name=":video_game: 놀이", value=f"따라해, 뽑기", inline=False)
    embed.add_field(name=":page_with_curl: 일반", value=f"내정보, 봇정보", inline=False)
    embed.add_field(name=":mag_right: 검색", value=f"유튜브, 이미지, 아바타", inline=False)
    embed.add_field(name=":desktop: 재깨봇 공식 사이트", value="[바로가기](https://jkbot.xyz)", inline=False)
    await ctx.reply(embed=embed, mention_author=False)


@client.command()
async def 아바타(ctx, user: discord.User):
    embed = discord.Embed(color=0xb5fb94, description=f"[링크]({user.avatar_url})")
    embed.set_author(name=user.name)
    embed.set_image(url=user.avatar_url)
    await ctx.reply(embed=embed, mention_author=False)


@client.command(aliases=["youtube", "유튭"])
async def 유튜브(ctx, *, search):
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://youtube.com/results?' + query_string

    )
    search_results = re.findall(r"watch\?v=(\S{11})", htm_content.read().decode())
    await ctx.reply('https://youtube.com/watch?v=' + search_results[0], mention_author=False)

#hellothisisverification

@client.command()
async def hellothisisverification(ctx):
    await ctx.send("⅄ooWıu#5973 (433183785564110848)")


@client.command()
async def 개발자(ctx):
    await ctx.send("유민#5973")



@client.command()
async def 따라해(ctx, *, text):
    await ctx.send(text)


@client.command()
async def 뽑기(ctx):
    ran = randint(1, 9)
    await ctx.reply(embed=discord.Embed(title=f'뽑기에서 {ran}이(가) 나왔습니다.', color=0xb5fb94, mention_author=False))


@client.command()
async def 청소(ctx, number:int=None):
    if ctx.guild:
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.reply('숫자를 입력해주세요.')
                elif 100 < number:
                    await ctx.message.delete()
                    await ctx.send(f'{ctx.message.author.mention} 100보다 큰 수는 입력할 수 없습니다.', delete_after=5)
                else:
                    deleted = await ctx.message.channel.purge(limit=number)
                    await ctx.send(f'{ctx.message.author.mention}에 의해 {len(deleted)}개의 메세지가 삭제되었습니다.')
            except:
              await ctx.reply("삭제가 불가합니다.")
        else:
          await ctx.reply('이 명령을 사용할 수 있는 권한이 없습니다.')
    else:
      await ctx.reply('DM에선 불가합니다.')


@client.command(aliases=["info", "정보"])
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


@client.command(aliases=["botinfo", "재깨봇"])
async def 봇정보(ctx):
    embed = discord.Embed(color=0xb5fb94)
    embed.set_author(name="재깨봇 정보", icon_url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.set_thumbnail(url="https://i.ibb.co/M71ftRF/image.jpg")
    embed.add_field(name="개발자", value="유민#5973", inline=False)
    embed.add_field(name="재깨봇 생일", value=f"2021년 5월 28일", inline=False)
    embed.add_field(name="사이트", value=f"[바로가기](https://jkbot.xyz)", inline=False)
    embed.add_field(name="한디리", value=f"[바로가기](https://bit.ly/kor_jkbot) <-하트 눌러주세요!", inline=False)
    embed.add_field(name="재깨봇 공식 서버", value=f"[바로가기](https://discord.ggB6MjFDjz23)", inline=False)
    await ctx.reply(embed=embed, mention_author=False)


@client.command(aliases=["img", "사진", "photo"])
async def 이미지(ctx, *, search):
    ran = randint(0, 9)
    resource = build("customsearch", "v1", developerKey=api_key).cse()
    result = resource.list(
        q=f"{search}", cx="cx", searchType="image"
    ).execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"`{search}`을(를) 검색했을때 결과입니다.", color=0xb5fb94)
    embed1.set_image(url=url)
    await ctx.reply(embed=embed1, mention_author=False)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
      em = discord.Embed(title=f"명령어를 찾을수 없습니다!", description="`,명령어`를 이용해주세요.", color=0xffff77) 
      await ctx.send(embed=em)
      return
    raise error

client.run(TOKEN)
