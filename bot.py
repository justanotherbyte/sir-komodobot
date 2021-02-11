# bot.py
import os
from asyncpraw.reddit import Reddit
from discord.ext import commands, tasks
import discord
from discord.ext.commands.cooldowns import BucketType
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
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

dagpi = Client(os.getenv('DAGPI_TOKEN'))
client = aiozaneapi.Client(os.getenv('ZANE_TOKEN'))

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._BotBase__cogs = commands.core._CaseInsensitiveDict()

async def get_prefix(bot, message):
    try:
        db = await aiosqlite.connect('config.db')
        cursor = await db.execute(f'SELECT prefix FROM config WHERE guild_id = {message.guild.id}')
        prefix = await cursor.fetchone()
        return prefix if prefix else "kb+"
    except:
        return 'kb+'
intents = discord.Intents.all()
bot = Bot(command_prefix=get_prefix, case_insensitive=True, intents=intents, )
bot.remove_command('help')



id = os.getenv('REDDIT_CLIENT_ID')
secret = os.getenv('REDDIT_CLIENT_SECRET')


message_cooldown = commands.CooldownMapping.from_cooldown(1.0, 3.0, commands.BucketType.user)

reddit = asyncpraw.Reddit(client_id=id, client_secret=secret, user_agent="Sir Komodo the Great Bot",)


@bot.command()
async def pixel(ctx, member: discord.Member):
    url = str(member.avatar_url_as(
        format="png", static_format="png", size=1024))
    img = await dagpi.image_process(ImageFeatures.pixel(), url)
    file = discord.File(fp=img.image, filename=f"pixel.{img.format}")
    await ctx.send(file=file)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='Listening for kb+help'))

@bot.command()
async def servers(ctx):
    activeservers = bot.guilds
    for guild in activeservers:
        await ctx.send(f"{guild.name}: {guild.id}")

class MyHelp(commands.MinimalHelpCommand):
    async def send_command_help(self, command): 
        ctx = self.context
        embed = discord.Embed(title=self.get_command_signature(command))
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)
        embed.add_field(name="Examples", value='`' + ctx.prefix + command.brief + '`', inline=False)
        channel = self.get_destination()
        await channel.send(embed=embed)
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page)
            await destination.send(embed=emby)
            

bot.help_command = MyHelp()


@bot.event
async def on_guild_join(guild):
    db = await aiosqlite.connect('config.db')
    await db.execute(f"insert into config values ({guild.id}, '!', 'enabled', 'enabled', 'enabled' )")
    await db.commit()



@bot.command(name='hello')
async def hello(ctx):
    member = ctx.author.mention
    await ctx.send(f'Hello, {member}! How are you today?')


@bot.command(description='Makes text bold')
async def bold(ctx, *, message):
    await ctx.send(f'**{message}**')


@bot.command(description='Sets the prefix for Sir KomodoBot to use in your server.')
async def setprefix(ctx, prefix: str):
    db = await aiosqlite.connect('config.db')
    await db.execute(f'update config set prefix = (?) where guild_id = {ctx.guild.id}', (prefix,))
    await db.commit()



@bot.command(description='sends the pog emote')
async def pog(ctx):
    await ctx.send('<:poggers:801548798424907816>')


@bot.command(description='Kicks a member, Admin Only')
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'User {member} has kicked.')




@bot.command(description='Asks specfified user to review the rules.')
async def rules(ctx, member: discord.Member):
    rules_channel = discord.utils.find(lambda m: "rule" in m.name, ctx.guild.channels)
    if not rules_channel is None:
        await member.send(f'{member.mention}, Please review the rules at <#{rules_channel.id}>')

@bot.command(name="emojify")
async def emojify(ctx, *, message):
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
    embed = discord.Embed(title="User Muted!", description="**{0}** was muted by **{1}** for {2}!".format(member, ctx.message.author, time), color=0xff00f6)
    await ctx.send(embed=embed)
    await asyncio.sleep(time)
    await member.add_roles(remove)
    await member.remove_roles(role)
    embed = discord.Embed(title="User Unmuted", description="**{0}** was muted by **{1}**!".format(member, ctx.message.author), color=0xff00f6)


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.author.bot:
        return
    if message.guild.id == 336642139381301249:
        return
    if ':' in message.content:
        string = message.content
        list_of_words = string.split()
        message_to_send = []
        ctx = await bot.get_context(message)
        for i in list_of_words:
            converter = commands.EmojiConverter()
            if i.startswith(':'):
                emoji_to_convert = i.strip(':')
                emoji =  await converter.convert(ctx, emoji_to_convert)
                message_to_send.append(str(emoji))
            else:
                message_to_send.append(i)
        await message.delete()
        webhook_message_to_send = ' '.join(message_to_send)
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


@bot.command(aliases=["pander", "pando"])
async def panda(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/img/panda") as r:
            res = await r.json()
    embed = discord.Embed(title=f"PANDA!!!", color=0x0000FF)
    embed.set_image(url=res["link"])
    embed.set_footer(text="Powered by https://some-random-api.ml")
    await ctx.send(embed=embed)

@bot.command(aliases=["bird", "birdo", "birbo"])
async def birb(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/img/birb") as r:
            res = await r.json()
    embed = discord.Embed(title=f"BIRB!!!", color=0x0000FF)
    embed.set_image(url=res["link"])
    embed.set_footer(text="Powered by https://some-random-api.ml")
    await ctx.send(embed=embed)

@bot.command(aliases=["foxo", "foxxo", "foxy", "foxxy"])
async def fox(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/img/fox") as r:
            res = await r.json()
    embed = discord.Embed(title=f"FOXXY!!!", color=0x0000FF)
    embed.set_image(url=res["link"])
    embed.set_footer(text="Powered by https://some-random-api.ml")
    await ctx.send(embed=embed)

@bot.command(aliases=["redpando", "redpander"])
async def redpanda(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/img/red_panda") as r:
            res = await r.json()
    embed = discord.Embed(title=f"RED PANDO!!!", color=0x0000FF)
    embed.set_image(url=res["link"])
    embed.set_footer(text="Powered by https://some-random-api.ml")
    await ctx.send(embed=embed)

@bot.command(aliases=["koaler"])
async def koala(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get("https://some-random-api.ml/img/koala") as r:
            res = await r.json()
    embed = discord.Embed(title=f"KOALA!!!", color=0x0000FF)
    embed.set_image(url=res["link"])
    embed.set_footer(text="Powered by https://some-random-api.ml")
    await ctx.send(embed=embed)
    

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
    else:
        await ctx.send(error.args[0])

    raise error


@bot.command(aliases=["dog", "doggy"])
async def doggo(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
            res = await r.json()
    embed = discord.Embed(title=f"DOGGO!!!", color=0xff0000)
    embed.set_image(url=res["message"])
    embed.set_footer(text="Powered by https://dog.ceo")
    await ctx.send(embed=embed)

@bot.command()
async def xkcd(ctx):
    comic_num = random.randint(1, 2415)
    async with aiohttp.ClientSession() as cs:
        async with cs.get(f'https://xkcd.com/{comic_num}/info.0.json') as r:
            res = await r.json()
    embed = discord.Embed(title=f"**{comic_num}: {res['title']}**", colour=discord.Colour(0xffffff), url=f"https://xkcd.com/{comic_num}/", description=res['alt'])
    embed.set_image(url=res["img"])
    embed.set_author(name="XKCD", url="https://xkcd.com", icon_url="https://cdn.changelog.com/uploads/icons/news_sources/P2m/icon_small.png?v=63722746912")
    embed.set_footer(
        text=f"Comic Released on: {res['month']}/{res['day']}/{res['year']} (view more comics at https://xkcd.com)")
    await ctx.send(embed=embed)
@bot.command()
@commands.cooldown(1, 3.0, BucketType.member)
async def meme(ctx):
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


@bot.command(description='gives you some cute animal pics!', aliases=['cute', 'awww'])
async def aww(ctx):
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

@bot.command()
async def gif(ctx, *, img, num=1):
    img = img.replace(" ", "+")
    async with aiohttp.ClientSession() as cs:
        link = f"http://api.giphy.com/v1/gifs/search?q={img}&api_key=0wltGsImBHY0GZGudUZG8aa6xybPJDit&limit={img}"
        async with cs.get(link) as r:
            res = await r.json()
            await ctx.send(res["data"][num-1]["url"])



@bot.command()
async def facepalm(ctx):
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

@bot.command(aliases=["ducc", "ducco", "ducko"])
async def duck(ctx):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://random-d.uk/api/random') as r:
            res = await r.json()
    embed = discord.Embed(title=f"DUCCCY!!!", color=0x0000ff)
    embed.set_image(url=res["url"])
    embed.set_footer(text=res["message"])
    await ctx.send(embed=embed)

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
                        embed2.add_field(name="**Active**", value=active, inline=True)
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

                        await ctx.send(embed=embed2)

        except:
            embed3 = discord.Embed(title="Invalid Country Name Or API Error! Try Again..!",
                                    colour=discord.Colour.blurple(), timestamp=ctx.message.created_at)
            embed3.set_author(name="Error!")
            await ctx.send(embed=embed3)

@bot.command()
async def magic(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    image = await client.magic(str(member.avatar_url_as(format='png')))
    file = discord.File(image, 'magic.gif')
    await ctx.send(file=file)
@bot.command()
async def deepfry(ctx, thing: typing.Union[discord.Member, discord.PartialEmoji, discord.Emoji, str]=None):
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
    file = discord.File(fp=img.image,filename=f"pixel.{img.format}")
    await ctx.send(file=file)

@bot.command()
async def leave(ctx):
    await ctx.guild.leave()

@bot.command()
async def info(ctx):
    p = pathlib.Path('./')
    cm = cr = fn = cl = ls = fc = 0
    for f in p.rglob('*.py'):
        if str(f).startswith("venv"):
            continue
        fc += 1
        with f.open() as of:
            for l in of.readlines():
                l = l.strip()
                if l.startswith('class'):
                    cl += 1
                if l.startswith('def'):
                    fn += 1
                if l.startswith('async def'):
                    cr += 1
                if '#' in l:
                    cm += 1
                ls += 1
    await ctx.send(f"file: {fc}\nline: {ls:,}\nclass: {cl}\nfunction: {fn}\ncoroutine: {cr}\ncomment: {cm:,}")

extensions = ['Jokes', 'Utility']

for extension in extensions:
    bot.load_extension(f"Cogs.{extension}")

bot.load_extension('jishaku')

bot.run(TOKEN)
