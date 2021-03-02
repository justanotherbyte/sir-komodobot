import discord
from discord.ext import commands
import asyncpg

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def start(self, ctx):
        