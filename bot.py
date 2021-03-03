# bot.py
import os
from asyncpraw.reddit import Reddit
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
import random
import asyncio
import re
import aiohttp
import asyncpraw
import aiosqlite
from bs4 import BeautifulSoup
import datetime
from asyncdagpi import ImageFeatures, Client
import aiozaneapi
import typing
import pathlib
from simpleeval import simple_eval
import async_cleverbot as ac
import psutil
import humanize
import time
import unicodedata
import similar
import inspect
from jishaku.functools import executor_function
import googletrans
import asyncpg
import sys
from difflib import get_close_matches
from fuzzywuzzy import process
from utils.HelpPaginator import CannotPaginate, HelpPaginator
import difflib
import traceback
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

dagpi = Client(os.getenv('DAGPI_TOKEN'))
cleverbot = ac.Cleverbot(os.getenv('CHATBOT_TOKEN'))


client = aiozaneapi.Client(os.getenv('ZANE_TOKEN'))


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()


async def get_prefix(bot, message):
    try:
        cursor = await bot.db.execute(f'SELECT prefix FROM config WHERE guild_id = {message.guild.id}')
        prefix = await cursor.fetchone()
        return prefix if prefix else "kb+"
    except:
        return 'kb+'
intents = discord.Intents.all()
bot = Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, )
bot.db = bot.loop.run_until_complete(aiosqlite.connect('config.db'))
#bot.economy = bot.loop.run_until_complete(asyncpg.connect('postgresql://'))
bot.remove_command('help')
bot.session = aiohttp.ClientSession(
    headers={"User-Agent": f"python-requests/2.25.1 The Anime Bot/1.1.0 Python/{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} aiohttp/{aiohttp.__version__}"})


message_cooldown = commands.CooldownMapping.from_cooldown(
    1.0, 3.0, commands.BucketType.user)


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='Listening for kb+help'))


@bot.command()
@commands.is_owner()
async def servers(ctx):
    activeservers = bot.guilds
    for guild in activeservers:
        await ctx.send(f"{guild.name}: {guild.id}")

"""
class MyHelp(commands.MinimalHelpCommand):
    async def send_command_help(self, command):
        ctx = self.context
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.description)
        alias = command.aliases
        if alias:
            embed.add_field(
                name="Aliases", value=", ".join(alias), inline=False)
        embed.add_field(name="Examples", value='`' +
                        ctx.prefix + command.brief + '`', inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)


bot.help_command = MyHelp()
"""

@bot.event
async def on_guild_join(guild):
    db = await aiosqlite.connect('config.db')
    await db.execute(f"insert into config values ({guild.id}, 'kb+', 'enabled', 'enabled', 'enabled' )")
    await db.commit()


@bot.command(description='Sets the prefix for Sir KomodoBot to use in your server.')
async def setprefix(ctx, prefix: str):
    await bot.db.execute(f'update config set prefix = (?) where guild_id = {ctx.guild.id}', (prefix,))
    await bot.db.commit()


@bot.command(description='Kicks a member, Admin Only')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')


@bot.command(description='Asks specfified user to review the rules.')
async def rules(ctx, member: discord.Member):
    rules_channel = discord.utils.find(
        lambda m: "rule" in m.name, ctx.guild.channels)
    if not rules_channel is None:
        await member.send(f'{member.mention}, Please review the rules at <#{rules_channel.id}>')


@bot.command(name='maf', description='Solves easy maf equations')
async def maf(ctx, *, message):
    await ctx.send(simple_eval(message))


@bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, time, member: discord.Member, reason=None):
    time_dict = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800}
    time = time_dict[time[-1]] * int(time[:-1])
    role = discord.utils.get(member.guild.roles, name='Muted')
    remove = discord.utils.get(member.guild.roles, name='Regular Memers')
    await member.add_roles(role)
    await member.remove_roles(remove)
    embed = discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for {2}!".format(
        member, ctx.message.author, time), color=0xff00f6)
    await ctx.send(embed=embed)
    await asyncio.sleep(time)
    await member.add_roles(remove)
    await member.remove_roles(role)
    embed = discord.Embed(title="User Unmuted", description="**{0}** was muted by **{1}**!".format(
        member, ctx.message.author), color=0xff00f6)

"""
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if re.search('<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})', message.content):
        return
    if re.search(r':(.*?):', message.content):
        string = message.content
        list_of_words = string.split()
        message_to_send = []
        ctx = await bot.get_context(message)
        for i in list_of_words:
            converter = commands.EmojiConverter()
            if i.startswith(':'):
                    emoji_to_convert = i.strip(':')
                    emoji = await converter.convert(ctx, emoji_to_convert)
                    message_to_send.append(str(emoji))
            else:
                message_to_send.append(i)
        #await message.channel.send(message_to_send)
        await message.delete()
        webhook_message_to_send = ' '.join(message_to_send)
        #await ctx.send(webhook_message_to_send)            
        webhook = await message.channel.create_webhook(name='webhook')
        await webhook.send(content=webhook_message_to_send, username=message.author.display_name, avatar_url=message.author.avatar_url)
        await webhook.delete()
    bucket = message_cooldown.get_bucket(message)
    retry_after = bucket.update_rate_limit()
    custom_emojis = re.findall(
        r'<(?P<animated>a?):(?P<name>[a-zA-Z0-9_]{2,32}):(?P<id>[0-9]{18,22})>', message.content)
    var = message.content
    num_of_capital_letters = sum(x.isupper() for x in var) / len(var) * 100
    if retry_after:
        await message.delete()
        msg = await message.channel.send(f"{message.author.mention}, Stop Spamming!")
        await asyncio.sleep(0.5)
        await msg.delete()
    if re.findall(r'(?:https?://)?discord(?:(?:app)?.com/invite|.gg)/?[a-zA-Z0-9]+/?', message.content):
        await message.delete()
        msg = await message.channel.send(f"{message.author.mention}, Discord Invite Links ain't allowed!")
        await asyncio.sleep(0.5)
        await msg.delete()
    if len(custom_emojis) > 10:
        await message.delete()
        msg = await message.channel.send(f"{message.author.mention}, Stop spamming emojis!")
        await asyncio.sleep(0.5)
        await msg.delete()
    if num_of_capital_letters > 70:
        await message.delete()
        msg = await message.channel.send(f"{message.author.mention}, Stop sending all uppercase messages!")
        await asyncio.sleep(0.5)
        await msg.delete()
    if re.search('\[.*\]\(https?:\\.*\.*\)', message.content):
        webhook = await message.channel.create_webhook(name='webhook')
        await webhook.send(content=message.content, username=message.author.display_name, avatar_url=message.author.avatar_url)
        await webhook.delete()
    if len(re.findall(r"<@!?\d{18,18}>", message.content)) > 5:
        await message.delete()
        msg = await message.channel.send(f"{message.author.mention}, Stop spam pinging!")
        await asyncio.sleep(0.5)
        await msg.delete()
    await bot.process_commands(message)
"""


@bot.command()
async def purge(ctx, number, member: discord.Member = None):
    def mycheck(message):
        return message.author.id == member.id

    if member is None:
        await ctx.channel.purge(limit=int(number))
    else:
        await ctx.channel.purge(limit=int(number), check=mycheck)


@bot.command()
async def mock(ctx, *, text):
    output_text = ""
    for char in text:
        if char.isalpha():
            if random.random() > 0.5:
                output_text += char.upper()
            else:
                output_text += char.lower()
        else:
            output_text += char
    await ctx.send(output_text)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{error.param} is a required argument that is missing!')
    if isinstance(error, commands.CommandOnCooldown):
        msg = await ctx.send(f'{ctx.author.mention}, try running the command again after {round(error.retry_after)} seconds')
        await msg.delete()
    if isinstance(error, commands.CommandNotFound):
        cmd = ctx.invoked_with
        cmds = [cmd.name for cmd in bot.commands]
        # cmds = [cmd.name for cmd in bot.commands if not cmd.hidden] # use this to stop showing hidden commands as suggestions
        matches = get_close_matches(cmd, cmds)
        if len(matches) > 0:
            await ctx.send(f'Command "{cmd}" not found, maybe you meant "{matches[0]}"?')
        else:
          await ctx.send(f'Command "{cmd}" not found, use the help command to know what commands are available')
    raise error

@bot.listen('on_message')
async def on_message(message):
    if re.search(r';(.*?);', message.content):
        string = message.content
        list_of_words = string.split()
        message_to_send = []
        for i in list_of_words:
            if i.startswith(';'):
                emoji_to_convert = i.strip(';')
                emoji = str(process.extract(emoji_to_convert, bot.emojis, limit=1)[0][0])
                message_to_send.append(emoji)
            else:
                pass
        if message:
            await message.channel.send(" ".join(message_to_send))
        else: return


@bot.listen('on_message_edit')
async def on_message_edit(old, new):
    if old.embeds != []:
        return
    if new.embeds != []:
        return
    await bot.process_commands(new)

@bot.command()
async def xkcd(ctx):
    comic_num = random.randint(1, 2415)
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://xkcd.com/{comic_num}/info.0.json') as r:
            res = await r.json()
    embed = discord.Embed(title=f"**{comic_num}: {res['title']}**", colour=discord.Colour(
        0xffffff), url=f"https://xkcd.com/{comic_num}/", description=res['alt'])
    embed.set_image(url=res["img"])
    embed.set_author(name="XKCD", url="https://xkcd.com",
                     icon_url="https://cdn.changelog.com/uploads/icons/news_sources/P2m/icon_small.png?v=63722746912")
    embed.set_footer(
        text=f"Comic Released on: {res['month']}/{res['day']}/{res['year']} (view more comics at https://xkcd.com)")
    await ctx.send(embed=embed)


@bot.command()
async def gif(ctx, *, img, num=1):
    img = img.replace(" ", "+")
    async with aiohttp.ClientSession() as cs:
        link = f"http://api.giphy.com/v1/gifs/search?q={img}&api_key=0wltGsImBHY0GZGudUZG8aa6xybPJDit&limit={img}"
        async with cs.get(link) as r:
            res = await r.json()
            img = res["data"][num-1]["url"]
            await ctx.send(f'{img}\nhttps://user-images.githubusercontent.com/74436682/108932641-8e088c80-75fe-11eb-9d69-da16519a41a8.png')


@bot.command(help='Posts a random bignate comic', brief='bignate')
async def bignate(ctx):
    start_date = datetime.date(1991, 2, 1)
    end_date = datetime.date(2020, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    date = str(random_date).replace('-', '/')
    async with aiohttp.ClientSession() as session:
        async with session.get(f'http://gocomics.com/bignate/{date}') as r:
            await ctx.trigger_typing()
            data = await r.text()
            soup = BeautifulSoup(data, 'html.parser')
            comic = soup.find('picture', class_='item-comic-image')
            embed = discord.Embed(
                title=comic.img['alt'], color=0x0000ff, url=f'http://gocomics.com/bignate/{date}')
            embed.set_image(url=comic.img['src'])
            await ctx.send(embed=embed)


@bot.command(help="Covid stats. Use world as country to view total stats", aliases=['cv'])
async def covid(ctx, *, countryName=None):
    try:
        if countryName is None:
            embed = discord.Embed(title=f"This command is used like this: ```{ctx.prefix}covid [country]```", colour=discord.Colour.blurple(
            ), timestamp=ctx.message.created_at)
            await ctx.send(embed=embed)

        else:
            await ctx.trigger_typing()
            url = f"https://coronavirus-19-api.herokuapp.com/countries/{countryName}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    json_stats = await r.json()
                    country = json_stats["country"]
                    totalCases = f'{json_stats["cases"]:,}'
                    todayCases = f'{json_stats["todayCases"]:,}'
                    totalDeaths = f'{json_stats["deaths"]:,}'
                    todayDeaths = f'{json_stats["todayDeaths"]:,}'
                    recovered = f'{json_stats["recovered"]:,}'
                    active = f'{json_stats["active"]:,}'
                    critical = f'{json_stats["critical"]:,}'
                    casesPerOneMillion = f'{json_stats["casesPerOneMillion"]:,}'
                    deathsPerOneMillion = f'{json_stats["deathsPerOneMillion"]:,}'
                    totalTests = f'{json_stats["totalTests"]:,}'
                    testsPerOneMillion = f'{json_stats["testsPerOneMillion"]:,}'

                    embed2 = discord.Embed(
                        title=f"**COVID-19 Status Of {country}**!", description="This Information Isn't Live Always, Hence It May Not Be Accurate!", colour=discord.Colour.blurple(), timestamp=ctx.message.created_at)
                    embed2.add_field(name="**Total Cases**",
                                     value=totalCases, inline=True)
                    embed2.add_field(name="**Today Cases**",
                                     value=todayCases, inline=True)
                    embed2.add_field(name="**Total Deaths**",
                                     value=totalDeaths, inline=True)
                    embed2.add_field(name="**Today Deaths**",
                                     value=todayDeaths, inline=True)
                    embed2.add_field(name="**Recovered**",
                                     value=recovered, inline=True)
                    embed2.add_field(name="**Active**",
                                     value=active, inline=True)
                    embed2.add_field(name="**Critical**",
                                     value=critical, inline=True)
                    embed2.add_field(name="**Cases Per One Million**",
                                     value=casesPerOneMillion, inline=True)
                    embed2.add_field(name="**Deaths Per One Million**",
                                     value=deathsPerOneMillion, inline=True)
                    embed2.add_field(name="**Total Tests**",
                                     value=totalTests, inline=True)
                    embed2.add_field(name="**Tests Per One Million**",
                                     value=testsPerOneMillion, inline=True)
                    embed2.set_footer(
                        text=f'Requested by {ctx.author.name}', icon_url=ctx.author.avatar_url)

                    await ctx.send(embed=embed2)

    except:
        embed3 = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!",
                               colour=discord.Colour.blurple(), timestamp=ctx.message.created_at)
        embed3.set_author(name="Error!")
        await ctx.send(embed=embed3)


@bot.command()
async def magic(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.author
    image = await client.magic(str(member.avatar_url_as(format='png')))
    file = discord.File(image, 'magic.gif')
    await ctx.send(file=file)


@bot.command()
async def leave(ctx):
    await ctx.guild.leave()




@bot.command()
async def cb(ctx, emotion='neutral'):
    emotions = {
        'neutral': ac.Emotion.neutral
    }
    await ctx.reply('Your chatbot session has started. Type `stop` to end it.')
    while True:
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        text = await bot.wait_for('message', check=check)
        if not (3 <= len(text.content) <= 60):
            await ctx.send("Text must be longer than 3 chars and shorter than 60.")
        else:
            async with ctx.channel.typing():
                response = await cleverbot.ask(text.content, emotion=emotions[f'{emotion}'])
                await text.reply(response)
                if text.content == 'stop':
                    await text.reply('Your chatbot session has ended')
                    break


@bot.command()
async def xkcdsearch(ctx, *, search):
    relevant_xkcd_url = 'https://relevantxkcd.appspot.com/process?action=xkcd&query='
    search_url = relevant_xkcd_url + search
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as resp:
            text = await resp.text()
            results = text.split('\n')
            num = results[2].split(' ')[0]
            async with aiohttp.ClientSession() as xkcd_session:
                async with xkcd_session.get(f'https://xkcd.com/{num}/info.0.json') as info:
                    comix = await info.json()
            more_results = f'[More results]({search_url})'
            round_relevance = round(float(results[0])*1000, 1)
            relevance = f'**Relevance: {round_relevance}%**'
            embed = discord.Embed(title=f"**{num}: {comix['title']}**", colour=discord.Colour(
                0xffffff), url=f"https://xkcd.com/{num}/", description=comix['alt'])
            embed.set_image(url=comix["img"])
            embed.set_author(name="XKCD", url="https://xkcd.com",
                             icon_url="https://cdn.changelog.com/uploads/icons/news_sources/P2m/icon_small.png?v=63722746912")
            embed.set_footer(
                text=f"Comic Released on: {comix['month']}/{comix['day']}/{comix['year']} (view more comics at https://xkcd.com)")
            await ctx.send(f'{relevance}', embed=embed)


@bot.command()
async def snipe(ctx):
    await ctx.send('Snipe Bad, I wont do it. People delet messages for reson, why u tryna peek at them? <:angery:747680299311300639>')


@bot.command()
async def charinfo(ctx, *, characters: str):
    """Shows you information about a number of characters.
    Only up to 25 characters at a time.
    """
    def to_string(c):
        digit = f'{ord(c):x}'
        name = unicodedata.name(c, 'Name not found.')
        return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
    msg = '\n'.join(map(to_string, characters))
    if len(msg) > 2000:
        return await ctx.send('Output too long to display.')
    await ctx.send(msg)


@bot.command()
async def getpic(ctx, url: str):
    try:
        link = url.strip('<')
        await ctx.send(f'https://image.thum.io/get/{url}')
    except:
        await ctx.send('Couldn\'t screenshot due to error')

#Credit to cryptex for help command
@bot.command(name="help")
async def _help(ctx, *, command: str = None):
    """Shows help about a command or the bot"""
    try:
        if command is None:
            p = await HelpPaginator.from_bot(ctx)
        else:
            entity = bot.get_cog(command) or bot.get_command(command)

            if entity is None:
                clean = command.replace('@', '@\u200b')
                failed_command = re.match(f"^({ctx.prefix})\s*(.*)",
                                          f"ovo {clean}",
                                          flags=re.IGNORECASE).group(2)
                matches = difflib.get_close_matches(failed_command,
                                                    ctx.bot.command_list)
                if not matches:
                    return
                return await ctx.send(
                    f"Command or category '{clean}' not found. Did you mean `{matches[0]}`?"
                )
            elif isinstance(entity, commands.Command):
                p = await HelpPaginator.from_command(ctx, entity)
            else:
                p = await HelpPaginator.from_cog(ctx, entity)

        await p.paginate()
    except Exception as error:
        print('Ignoring exception in command {}:'.format(ctx.command),
              file=sys.stderr)
        traceback.print_exception(type(error),
                                  error,
                                  error.__traceback__,
                                  file=sys.stderr)

@bot.command()
async def redirectcheck(ctx, website):
    website = website.strip("<>")
    async with aiohttp.ClientSession(headers={'User-Agent': 'python-requests/2.20.0'}).get(website) as resp:
        soup = BeautifulSoup(await resp.text(), features="lxml")
        canonical = soup.find('link', {'rel': 'canonical'})
        if canonical == None:
            return await ctx.send(f"`{resp.real_url}`")
        await ctx.send(f"`{canonical['href']}`")


@bot.command(aliases=['src'])
async def source(ctx):
    embed = discord.Embed(title='Sir KomodoBot\'s Source')
    embed.description = 'Here is my repo link: https://github.com/MrKomodoDragon/sir-komodobot\n\nDon\'t forget to leave a star!\n(Also, [please respect the license!](https://github.com/MrKomodoDragon/sir-komodobot/blob/main/LICENSE))'
    await ctx.send(embed=embed)


@bot.command()
async def halptest(ctx):
    page_embed = discord.Embed()
    page_embed.title = "Help command"
    page_embed.description = "```<> means argument is required\n[]means argument is optional```\nReact with 🥳 to view the commands for fun, and react with 🏠 to go back to the home page. React with "
    fun_embed = discord.Embed()
    cog = bot.get_cog('Fun').get_commands()
    for cmd in cog:
        alias = cmd.aliases
        if alias:
            fun_embed.add_field(name=f'{cmd.name} {cmd.signature}',
                                value=f'What it does: {cmd.description}\nAliases: {", ".join(alias)}\nExample: {ctx.prefix}{cmd.brief}')   # ", ".join(alias)
        else:
            fun_embed.add_field(name=f'{cmd.name} {cmd.signature}',
                                value=f'What it does: {cmd.description}\nExample: {ctx.prefix}{cmd.brief}')

    mesage = await ctx.send(embed=page_embed)
    await mesage.add_reaction('🏠')
    await mesage.add_reaction('🥳')

    def check(reaction, user):
        return str(reaction.emoji) in ['🥳', '🏠'] and user == ctx.author

    def check_remove(reaction_remove, user_remove):
        return str(reaction_remove.emoji) in ['🥳', '🏠'] and user_remove == ctx.author
    while True:
        reaction, user = await bot.wait_for('reaction_add', check=check)
        if str(reaction.emoji) == '🥳':
            await mesage.edit(embed=fun_embed)
            await mesage.remove_reaction('🥳', ctx.author)
        if str(reaction.emoji) == '🏠':
            await mesage.edit(embed=page_embed)
            await mesage.remove_reaction('🏠', ctx.author)


extensions = ['Fun', 'Utility', 'Images', 'jishaku', 'Socket', 'Music']

for extension in extensions:
    bot.load_extension(f"Cogs.{extension}")


bot.run(TOKEN)
