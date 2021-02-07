
import asyncpraw
import aiohttp
import re
import asyncio
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os


class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Checks Latency of Bot")
    async def ping(self, ctx):
        x = await ctx.send('Pong!')
        ping = round(self.bot.latency*1000)
        content1 = f'Pong! `{ping}ms`'
        await x.edit(content=str(content1))


def setup(bot):
    bot.add_cog(Utility(bot))
