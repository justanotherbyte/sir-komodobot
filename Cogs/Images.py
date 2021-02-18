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
    async def pixel(ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing == None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, discord.PartialEmoji) or isinstance(thing, discord.Emoji):
                url = str(thing.url)
            elif isinstance(thing, discord.Member) or isinstance(thing, discord.User):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
            img = await dagpi.image_process(ImageFeatures.pixel(), url)
            file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
            await ctx.send(file=file)
        
    @commands.command()
    async def deepfry(ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str] = None):
        async with ctx.channel.typing():
            if thing == None:
                url = str(ctx.author.avatar_url_as(static_format="png"))
            elif isinstance(thing, discord.PartialEmoji) or isinstance(thing, discord.Emoji):
                url = str(thing.url)
            elif isinstance(thing, discord.Member) or isinstance(thing, discord.User):
                url = str(thing.avatar_url_as(static_format="png"))
            else:
                url = thing
        img = await dagpi.image_process(ImageFeatures.deepfry(), url)
        file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
        await ctx.send(file=file)

def setup(bot):
    bot.add_cog(Images(bot))