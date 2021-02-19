
import asyncpraw
import aiohttp
import re
import asyncio
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands, tasks
import os
from utils import fuzzy
import zlib
import io

#Everything Related to the rtfm command, I took from Robo Danny. Check out the bot at https://github.com/Rapptz/RoboDanny


class SphinxObjectFileReader:
    BUFSIZE = 16 * 1024

    def __init__(self, buffer):
        self.stream = io.BytesIO(buffer)

    def readline(self):
        return self.stream.readline().decode('utf-8')

    def skipline(self):
        self.stream.readline()

    def read_compressed_chunks(self):
        decompressor = zlib.decompressobj()
        while True:
            chunk = self.stream.read(self.BUFSIZE)
            if len(chunk) == 0:
                break
            yield decompressor.decompress(chunk)
        yield decompressor.flush()

    def read_compressed_lines(self):
        buf = b''
        for chunk in self.read_compressed_chunks():
            buf += chunk
            pos = buf.find(b'\n')
            while pos != -1:
                yield buf[:pos].decode('utf-8')
                buf = buf[pos + 1:]
                pos = buf.find(b'\n')



class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'python': 'https://docs.python.org/3',
            'asyncpg': "https://magicstack.github.io/asyncpg/current/",
            "zaneapi": "https://docs.zaneapi.com/en/latest/",
            "aiohttp": "https://docs.aiohttp.org/en/stable/"
        }
        bot.loop.create_task(
            self.build_rtfm_lookup_table(page_types=page_types))

    def parse_object_inv(self, stream, url):
        # key: URL
        # n.b.: key doesn't have `discord` or `discord.ext.commands` namespaces
        result = {}

        # first line is version info
        inv_version = stream.readline().rstrip()

        if inv_version != '# Sphinx inventory version 2':
            raise RuntimeError('Invalid objects.inv file version.')

        # next line is "# Project: <name>"
        # then after that is "# Version: <version>"
        projname = stream.readline().rstrip()[11:]
        version = stream.readline().rstrip()[11:]

        # next line says if it's a zlib header
        line = stream.readline()
        if 'zlib' not in line:
            raise RuntimeError(
                'Invalid objects.inv file, not z-lib compatible.')

        # This code mostly comes from the Sphinx repository.
        entry_regex = re.compile(
            r'(?x)(.+?)\s+(\S*:\S*)\s+(-?\d+)\s+(\S+)\s+(.*)')
        for line in stream.read_compressed_lines():
            match = entry_regex.match(line.rstrip())
            if not match:
                continue

            name, directive, prio, location, dispname = match.groups()
            domain, _, subdirective = directive.partition(':')
            if directive == 'py:module' and name in result:
                # From the Sphinx Repository:
                # due to a bug in 1.1 and below,
                # two inventory entries are created
                # for Python modules, and the first
                # one is correct
                continue

            # Most documentation pages have a label
            if directive == 'std:doc':
                subdirective = 'label'

            if location.endswith('$'):
                location = location[:-1] + name

            key = name if dispname == '-' else dispname
            prefix = f'{subdirective}:' if domain == 'std' else ''

            if projname == 'discord.py':
                key = key.replace('discord.ext.commands.',
                                  '').replace('discord.', '')

            result[f'{prefix}{key}'] = os.path.join(url, location)

        return result

    async def build_rtfm_lookup_table(self, page_types):
        cache = {}
        for key, page in page_types.items():
            sub = cache[key] = {}
            async with aiohttp.ClientSession().get(page +
                                                   '/objects.inv') as resp:
                if resp.status != 200:
                    raise RuntimeError(
                        'Cannot build rtfm lookup table, try again later.')

                stream = SphinxObjectFileReader(await resp.read())
                cache[key] = self.parse_object_inv(stream, page)

        self.bot._rtfm_cache = cache


    async def uhh_rtfm_pls(self, ctx, key, obj):
        page_types = {
            'latest': 'https://discordpy.readthedocs.io/en/latest',
            'python': 'https://docs.python.org/3',
            'asyncpg': "https://magicstack.github.io/asyncpg/current/",
            "zaneapi": "https://docs.zaneapi.com/en/latest/",
            "aiohttp": "https://docs.aiohttp.org/en/stable/"
        }
        if obj is None:
            await ctx.send(page_types[key])
            return

        if not hasattr(self.bot, "_rtfm_cache"):
            await ctx.trigger_typing()
            await self.build_rtfm_lookup_table(page_types)

        obj = re.sub(r'^(?:discord\.(?:ext\.)?)?(?:commands\.)?(.+)', r'\1',
                     obj)

        if key.startswith('latest'):
            # point the abc.Messageable types properly:
            q = obj.lower()
            for name in dir(discord.abc.Messageable):
                if name[0] == '_':
                    continue
                if q == name:
                    obj = f'abc.Messageable.{name}'
                    break

        cache = list(self.bot._rtfm_cache[key].items())

        def transform(tup):
            return tup[0]

        matches = fuzzy.finder(obj, cache, key=lambda t: t[0], lazy=False)[:10]

        e = discord.Embed(colour=0x00ff6a)
        if len(matches) == 0:
            return await ctx.send("Can't find anything")

        e.description = '\n'.join(f'[`{key}`]({url})' for key, url in matches)
        await ctx.send(embed=e)

    @commands.command(description="Checks Latency of Bot")
    async def ping(self, ctx):
        x = await ctx.send('Pong!')
        ping = round(self.bot.latency*1000)
        content1 = f'Pong! `{ping}ms`'
        await x.edit(content=str(content1))

    @commands.group(invoke_without_command=True,
                    aliases=[
                        "read_the_fucking_manual", "rtfd",
                        "read_the_fucking_doc", "read_tfm", "read_tfd"
                    ])
    async def rtfm(self, ctx, *, thing: str = None):
        await self.uhh_rtfm_pls(ctx, "latest", thing)

    @rtfm.command(name="py", aliases=["python"])
    async def rtfm_py(self, ctx, *, thing: str = None):
        await self.uhh_rtfm_pls(ctx, "python", thing)

    @rtfm.command(name="asyncpg", aliases=["apg"])
    async def rtfm_asyncpg(self, ctx, *, thing: str = None):
        await self.uhh_rtfm_pls(ctx, "asyncpg", thing)

    @rtfm.command(name="zaneapi")
    async def rtfm_zaneapi(self, ctx, *, thing: str = None):
        await self.uhh_rtfm_pls(ctx, "zaneapi", thing)

    @rtfm.command(name="aiohttp")
    async def rtfm_aiohttp(self, ctx, *, thing: str = None):
        await self.uhh_rtfm_pls(ctx, "aiohttp", thing)



def setup(bot):
    bot.add_cog(Utility(bot))
