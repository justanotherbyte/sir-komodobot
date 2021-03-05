import discord
from discord.ext import commands
import asyncpg

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def register(self, ctx):
        try:
            value = self.bot.pg.fetchrow('SELECT * from economy where member_id = $1', ctx.author.id)
            if value != None:
                await ctx.send(embed=discord.Embed(description='You have already registered!'))
            else:                
                await self.bot.pg.execute('INSERT INTO economy VALUES($1, 500, 0)', ctx.author.id)
                await ctx.send(embed=discord.Embed(title='Success!', description=f'You have successfully registered. You currently have $500 in your wallet. Try running some commands in `{ctx.prefix}help economy to get some more money!'))
        except:
            await ctx.send(embed=discord.Embed(description='An error occured'))

def setup(bot):
    bot.add_cog(Economy(bot))