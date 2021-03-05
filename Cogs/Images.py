import inspect
import similar
import unicodedata
import time
import humanize
import psutil
import async_cleverbot as ac
from simpleeval import simple_eval
import pathlib
import typing
import aiozaneapi
from asyncdagpi import ImageFeatures, Client
import datetime
from bs4 import BeautifulSoup
import aiosqlite
import asyncpraw
import aiohttp
import re
import asyncio
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
from asyncpraw.reddit import Reddit
import os

load_dotenv()

dagpi = Client(os.getenv('DAGPI_TOKEN'))
client = aiozaneapi.Client(os.getenv('ZANE_TOKEN'))

class Images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def pixel(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
            img = await dagpi.image_process(ImageFeatures.pixel(), url)
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            await ctx.send(file=file)
        
    @commands.command()
    async def deepfry(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.deepfry(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def ascii(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.ascii(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def colors(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.colors(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def america(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.america(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def communism(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.communism(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def triggered(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.triggered(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def wasted(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.wasted(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def invert(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.invert(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def blur(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
                url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.blur(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def sobel(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.sobel(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def rgb(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.rgb(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def hog(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.hog(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def triangle(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.triangle(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command(aliases=['5g1g'])
    async def _5g1g(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str], thing2: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None,):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
            if thing2 is None:
                url2 = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing2, (discord.PartialEmoji, discord.Emoji)):
                url2 = str(thing2.url)
            elif isinstance(thing2, (discord.Member, discord.User)):
                url2 = str(thing2.avatar_url_as(static_format="png"))
            else:
                url2 = thing2
            url2 = url2.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.five_guys_one_girl(), url=url, url2=url2)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command(aliases=['gay'])
    async def why_are_u_gay(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str], thing2: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None,):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
            if thing2 is None:
                url2 = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing2, (discord.PartialEmoji, discord.Emoji)):
                url2 = str(thing2.url)
            elif isinstance(thing2, (discord.Member, discord.User)):
                url2 = str(thing2.avatar_url_as(static_format="png"))
            else:
                url2 = thing2
            url2 = url2.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.why_are_you_gay(), url=url, url2=url2)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def angel(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.angel(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def satan(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.satan(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def hitler(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.hitler(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def obama(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.obama(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def bad(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.bad(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def sith(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.sith(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def jail(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.jail(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)
    
    @commands.command()
    async def rainbow(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        img = await dagpi.image_process(ImageFeatures.rainbow(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

    @commands.command()
    async def magic(self, ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing is None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, (discord.PartialEmoji, discord.Emoji)):
                url = str(thing.url)
            elif isinstance(thing, (discord.Member, discord.User)):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            url = url.replace("cdn.discordapp.com", "media.discordapp.net")
        image = await client.magic(url)
        file = discord.File(image, 'magic.gif')
        await ctx.send(file=file)


def setup(bot):
    bot.add_cog(Images(bot))
