import os
from discord import client
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
import random
from discord.ext.commands.cooldowns import BucketType
import asyncio
import re
import aiohttp
import asyncpraw
from asyncdagpi import ImageFeatures, Client

load_dotenv()

id = os.getenv('REDDIT_CLIENT_ID')
secret = os.getenv('REDDIT_CLIENT_SECRET')

dagpi = Client(os.getenv('DAGPI_TOKEN'))

reddit = asyncpraw.Reddit(client_id=id, client_secret=secret, user_agent="Sir Komodo the Great Bot",)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Posts a random joke')
    async def joke(self, ctx):
        with open('jokes.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(description='Posts a random Knock-Knock Joke')
    async def knockknock(self, ctx):
        with open('knock-knock.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(description='Posts a dad-joke')
    async def dadjoke(self, ctx):
        with open('dadjokes.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(help='Posts a very *punny* pun', brief=f'pun')
    async def pun(self, ctx):
        with open('puns.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))

    @commands.command(description='Makes text bold')
    async def bold(self, ctx, *, message):
        await ctx.send(f'**{message}**')

    @commands.command(name="emojify")
    async def emojify(self, ctx, *, message):
        emojis = []
        message1 = message.lower()
        letters = list(message1)
        for i in letters:
            if i.isalpha():
                emojis.append(f':regional_indicator_{i}:')
            elif i == " ":
                emojis.append(' ')
            else:
                emojis.append(i)
        sentence = " ".join(emojis)
        await ctx.send(sentence)

    @commands.command(aliases=["pander", "pando"])
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"PANDA!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)


    @commands.command(aliases=["bird", "birdo", "birbo"])
    async def birb(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/birb") as r:
                res = await r.json()
        embed = discord.Embed(title=f"BIRB!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)


    @commands.command(aliases=["foxo", "foxxo", "foxy", "foxxy"])
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as r:
                res = await r.json()
        embed = discord.Embed(title=f"FOXXY!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)


    @commands.command(aliases=["redpando", "redpander"])
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/red_panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"RED PANDO!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)


    @commands.command(aliases=["koaler"])
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/koala") as r:
                res = await r.json()
        embed = discord.Embed(title=f"KOALA!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["cato"])
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/cat") as r:
                res = await r.json()
        embed = discord.Embed(title=f"CATTO!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(description='gives you some cute animal pics!', aliases=['cute', 'awww'])
    async def aww(self, ctx):
        subreddit = await reddit.subreddit("aww")
        submission = await subreddit.random()
        if not submission.over_18:
            titled = submission.title
            url = submission.url
            reddited = submission.subreddit_name_prefixed
            reddit_embed = discord.Embed(
                title=f"**{titled}**", url=f'https://reddit.com/comments/{submission.id}', color=discord.Colour.orange())
            reddit_embed.set_author(name=f"{reddited}", url=f'https://www.reddit.com/r/{subreddit}',
                                    icon_url='https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2')
            reddit_embed.set_image(url=f'{url}')
            await ctx.send(embed=reddit_embed)

    @commands.command(aliases=["dog", "doggy"])
    async def doggo(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DOGGO!!!", color=0xff0000)
        embed.set_image(url=res["message"])
        embed.set_footer(text="Powered by https://dog.ceo")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3.0, BucketType.member)
    async def meme(self, ctx):
        subreddit = await reddit.subreddit("memes")
        submission = await subreddit.random()
        if not submission.over_18:
            titled = submission.title
            url = submission.url
            reddited = submission.subreddit_name_prefixed
            reddit_embed = discord.Embed(
                title=f"**{titled}**", url=f'https://reddit.com/comments/{submission.id}', color=discord.Colour.orange())
            reddit_embed.set_author(name=f"{reddited}", url=f'https://www.reddit.com/r/{subreddit}',
                                    icon_url='https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2')
            reddit_embed.set_image(url=f'{url}')
            await ctx.trigger_typing()
            await ctx.send(embed=reddit_embed)
    @commands.command()
    async def facepalm(self, ctx):
        subreddit = await reddit.subreddit("facepalm")
        submission = await subreddit.random()
        if not submission.over_18:
            titled = submission.title
            url = submission.url
            reddited = submission.subreddit_name_prefixed
            reddit_embed = discord.Embed(
                title=f"**{titled}**", url=f'https://reddit.com/comments/{submission.id}', color=discord.Colour.orange())
            reddit_embed.set_author(name=f"{reddited}", url=f'https://www.reddit.com/r/{subreddit}',
                                    icon_url='https://external-preview.redd.it/iDdntscPf-nfWKqzHRGFmhVxZm4hZgaKe5oyFws-yzA.png?auto=webp&s=38648ef0dc2c3fce76d5e1d8639234d8da0152b2')
            reddit_embed.set_image(url=f'{url}')
            await ctx.send(embed=reddit_embed)


    @commands.command(aliases=["ducc", "ducco", "ducko"])
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random-d.uk/api/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DUCCCY!!!", color=0x0000ff)
        embed.set_image(url=res["url"])
        embed.set_footer(text=res["message"])
        await ctx.send(embed=embed)
    @commands.command()
    async def roast(self, ctx, member: discord.Member=None):
        if member == None:
            member =  ctx.author
        roast = await dagpi.roast()
        await ctx.send(f"**{member.name}**, {roast}")

def setup(bot):
    bot.add_cog(Fun(bot))
