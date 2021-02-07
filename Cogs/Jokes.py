import os
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
import random
from discord_slash import SlashCommand, SlashContext
import asyncio
import re
import aiohttp
import asyncpraw
class Jokes(commands.Cog):
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
def setup(bot):
    bot.add_cog(Jokes(bot))
