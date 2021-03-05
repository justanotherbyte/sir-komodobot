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
import similar
from utils.fuzzy import finder
from jishaku.paginators import WrappedPaginator, PaginatorInterface

load_dotenv()

id = os.getenv('REDDIT_CLIENT_ID')
secret = os.getenv('REDDIT_CLIENT_SECRET')

dagpi = Client(os.getenv('DAGPI_TOKEN'))

reddit = asyncpraw.Reddit(client_id=id, client_secret=secret, user_agent="Sir Komodo the Great Bot",)

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description='Posts a random joke', brief='joke')
    async def joke(self, ctx):
        with open('jokes.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(description='Posts a random Knock-Knock Joke', brief='knockknock')
    async def knockknock(self, ctx):
        with open('knock-knock.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(description='Posts a dad-joke', brief='dadjoke')
    async def dadjoke(self, ctx):
        with open('dadjokes.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))


    @commands.command(description='Posts a very *punny* pun', brief=f'pun')
    async def pun(self, ctx):
        with open('puns.txt', 'r') as f:
            jokes = list(f)
            await ctx.send(random.choice(jokes))

    @commands.command(description='Makes text bold', brief = 'bold hello')
    async def bold(self, ctx, *, message):
        await ctx.send(f'**{message}**')

    @commands.command(description='Turns text in to regional indicators', brief='emojify hello')
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

    @commands.command(aliases=["pander", "pando"], description='Look at some pandas', brief='panda')
    async def panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"PANDA!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)


    @commands.command(aliases=["bird", "birdo", "birbo"], description='Look at some birbs', brief='birb')
    async def birb(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/birb") as r:
                res = await r.json()
        embed = discord.Embed(title=f"BIRB!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["foxo", "foxxo", "foxy", "foxxy"], description='Look at some foxed', brief='fox')
    async def fox(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/fox") as r:
                res = await r.json()
        embed = discord.Embed(title=f"FOXXY!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["redpando", "redpander"], description='Look at some red pandas', brief='birb')
    async def redpanda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/red_panda") as r:
                res = await r.json()
        embed = discord.Embed(title=f"RED PANDO!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["koaler"], description='Look at some red pandas', brief='birb')
    async def koala(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/koala") as r:
                res = await r.json()
        embed = discord.Embed(title=f"KOALA!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(aliases=["cato"], description='Look at some red pandas', brief='birb')
    async def cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://some-random-api.ml/img/cat") as r:
                res = await r.json()
        embed = discord.Embed(title=f"CATTO!!!", color=0x0000FF)
        embed.set_image(url=res["link"])
        embed.set_footer(text="Powered by https://some-random-api.ml")
        await ctx.send(embed=embed)

    @commands.command(description='gives you some cute animal pics!', aliases=['cute', 'awww'], brief='aww')
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

    @commands.command(aliases=["dog", "doggy"], description='Look at some red pandas', brief='birb')
    async def doggo(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DOGGO!!!", color=0xff0000)
        embed.set_image(url=res["message"])
        embed.set_footer(text="Powered by https://dog.ceo")
        await ctx.send(embed=embed)

    class PaginatorEmbedInterface(PaginatorInterface):
        def __init__(self, *args, **kwargs):
            self._embed = discord.Embed()
            super().__init__(*args, **kwargs)

        @property
        def send_kwargs(self) -> dict:
            display_page = self.display_page
            self._embed.description = f"**:7298_Nitro_Gif: Emoji List**\n{self.pages[display_page]}"
            self._embed.set_footer(
                text=f'Page {display_page + 1}/{self.page_count}')
            return {'embed': self._embed}

        max_page_size = 2048

        @property
        def page_size(self) -> int:
            return self.paginator.max_size

    @commands.command(description='Look at some red pandas', brief='birb')
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

    @commands.command(description='Look at some red pandas', brief='birb')
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

    @commands.command(aliases=["ducc", "ducco", "ducko"], description='Look at some red pandas', brief='birb')
    async def duck(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get('https://random-d.uk/api/random') as r:
                res = await r.json()
        embed = discord.Embed(title=f"DUCCCY!!!", color=0x0000ff)
        embed.set_image(url=res["url"])
        embed.set_footer(text=res["message"])
        await ctx.send(embed=embed)

    @commands.command(description='Look at some red pandas', brief='birb')
    async def roast(self, ctx, member: discord.Member=None):
        if member is None:
            member =  ctx.author
        roast = await dagpi.roast()
        await ctx.send(f"**{member.name}**, {roast}")

    @commands.command(description='Look at some red pandas', brief='birb')
    async def top(ctx, subreddit):
        subreddit = await reddit.subreddit(subreddit)
        top_posts = subreddit.top("hour")
        await ctx.send(top_posts)
    
    @commands.command()
    async def emoji(self, ctx, *, search: str = None):
        lists = []
        paginator = WrappedPaginator(max_size=500, prefix="", suffix="")
        if search != None:
            emojis = finder(search,
                            self.bot.emojis,
                            key=lambda i: i.name,
                            lazy=False)
            if emojis == []:
                return await ctx.send("no emoji found")
            for i in emojis:
                if i.animated == True:
                    lists.append(f"{str(i)} `<a:{i.name}:{i.id}>`")
                else:
                    lists.append(f"{str(i)} `<:{i.name}:{i.id}>`")
            paginator.add_line("\n".join(lists))
            interface = self.PaginatorEmbedInterface(ctx.bot,
                                           paginator,
                                           owner=ctx.author)
            return await interface.send_to(ctx)
        for i in self.bot.emojis:
            if i.animated == True:
                lists.append(f"{str(i)} `<a:{i.name}:{i.id}>`")
            else:
                lists.append(f"{str(i)} `<:{i.name}:{i.id}>`")
        paginator.add_line("\n".join(lists))
        interface = self.PaginatorEmbedInterface(ctx.bot, paginator, owner=ctx.author)
        await interface.send_to(ctx)

    @commands.command()
    async def opt_in(self, ctx):
        opt_in = await self.bot.emotes.fetchrow('SELECT opt_in from emotes WHERE member_id = $1', ctx.author.id)
        opt_in = opt_in['opt_in']
        if opt_in == True:
            await ctx.send("You Have Already opted-in to emotes")
        else:
            await self.bot.emotes.execute('UPDATE emotes set opt_in = TRUE WHERE member_id = $1', ctx.author.id)
            await ctx.send("You have opted-in to emoji.")
    
    @commands.command()
    async def opt_out(self, ctx):
        opt_in = await self.bot.emotes.fetchrow('SELECT opt_in from emotes WHERE member_id = $1', ctx.author.id)
        opt_in = opt_in['opt_in']
        if opt_in == False:
            await ctx.send("You Have Already opted out of emotes")
        else:
            await self.bot.emotes.execute('UPDATE emotes set opt_in = FALSE WHERE member_id = $1', ctx.author.id)
            await ctx.send("You have opted out of emoji.")

def setup(bot):
    bot.add_cog(Fun(bot))
