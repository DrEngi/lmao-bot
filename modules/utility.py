import discord
from discord.ext import commands
from utils import usage, lbutil
import sys
import io
import json
import time
import math
import asyncio
import random as rand
from datetime import datetime
import urllib.parse
if sys.version < '3':
    from urllib2 import urlopen
    from urllib import quote as urlquote
else:
    from urllib.request import urlopen
    from urllib.parse import quote as urlquote

UD_DEFID_URL = 'http://api.urbandictionary.com/v0/define?defid='
UD_DEFINE_URL = 'http://api.urbandictionary.com/v0/define?term='
UD_RANDOM_URL = 'http://api.urbandictionary.com/v0/random'

class UrbanDefinition(object):
    def __init__(self, word, definition, example, upvotes, downvotes):
        self.word = word
        self.definition = definition
        self.example = example
        self.upvotes = upvotes
        self.downvotes = downvotes

    def __str__(self):
        return '%s: %s%s (%d, %d)' % (
                self.word,
                self.definition[:50],
                '...' if len(self.definition) > 50 else '',
                self.upvotes,
                self.downvotes
            )

def _get_urban_json(url):
    f = urlopen(url)
    data = json.loads(f.read().decode('utf-8'))
    f.close()
    return data

def _parse_urban_json(json, check_result=True):
    result = []
    if json is None or any(e in json for e in ('error', 'errors')):
        raise ValueException('UD: Invalid input for Urban Dictionary API')
    #if check_result and json['result_type'] == 'no_results':
    #    return result
    for definition in json['list']:
        d = UrbanDefinition(
                definition['word'],
                definition['definition'],
                definition['example'],
                int(definition['thumbs_up']),
                int(definition['thumbs_down'])
            )
        result.append(d)
    return result

def define(term):
    """Search for term/phrase and return list of UrbanDefinition objects.
    Keyword arguments:
    term -- term or phrase to search for (str)
    """
    json = _get_urban_json(UD_DEFINE_URL + urlquote(term))
    return _parse_urban_json(json)

def defineID(defid):
    """Search for UD's definition ID and return list of UrbanDefinition objects.
    Keyword arguments:
    defid -- definition ID to search for (int or str)
    """
    json = _get_urban_json(UD_DEFID_URL + urlquote(str(defid)))
    return _parse_urban_json(json)

def random():
    """Return random definitions as a list of UrbanDefinition objects."""
    json = _get_urban_json(UD_RANDOM_URL)
    return _parse_urban_json(json, check_result=False)

def lmgtfy(query):
    return "Let me Google that for you... http://lmgtfy.com/?q=" + urllib.parse.quote_plus(query)

class Utility:

    slots = ('bot')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="urban", aliases=["define", "dictionary", "urbandictionary", "ud"])
    async def cmd_urban(self, ctx, *, arg=""):
        await ctx.trigger_typing()
        if not ctx.message.channel.is_nsfw():
            await ctx.send(ctx.author.mention + " Whoa-ho-ho-ho, hold your horses. The Urban Dictionary command only works in NSFW channels.")
            return 'urban'
        try:
           urban_def = define(arg)[0]
           e = discord.Embed(title=f"**Urban Dictionary Entry for {urban_def.word}**")
           e.add_field(name="Definition", value=urban_def.definition)
           e.add_field(name="Example", value=urban_def.example)
           e.add_field(name="Upvotes 👍", value=urban_def.upvotes)
           e.add_field(name="Downvotes 👎", value=urban_def.downvotes)
           await ctx.send(embed=e)
        except IndexError:
           await ctx.send("Sorry, **{}** could not be found on Urban Dictionary.".format(arg))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="lmgtfy", aliases=["google", "search"])
    async def cmd_lmgtfy(self, ctx, *, arg=""):
        await ctx.trigger_typing()
        await ctx.send(lmgtfy(arg))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="vaporwave", aliases=["aesthetic"])
    async def cmd_vaporwave(self, ctx, *, text=""):
        if text.strip() == "":
            await ctx.send(f"{ctx.author.mention} You have to include TEXT you want to turn into ＴＥＸＴ. Use `{ctx.prefix}{ctx.invoked_with} text`.")
            usage.update(ctx)
            return ctx.command.name
        vapor_h = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&()*+,-./:;<=>?@[]^_`{|}~'
        vapor_f = '０１２３４５６７８９ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ！゛＃＄％＆（）＊＋、ー。／：；〈＝〉？＠［］＾＿‘｛｜｝～'
        transformed = text
        for i in range(0, len(vapor_h)):
            transformed = transformed.replace(vapor_h[i], vapor_f[i])
        # for i in range(0, len(text)):
        #     transformed += text[i] + " "
        await ctx.send(transformed[:2000])
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="remind", aliases=["remindme"])
    async def cmd_remind(self, ctx, *, arg=""):
        humor = [
            "Take cookies out of oven.",
            "Construct additional pylons.",
            "Download more RAM.",
            "Claim my free prize for being the millionth visitor."
        ]
        reminder = arg
        if reminder == "":
            await ctx.send(f"{ctx.author.mention} What do you want to be reminded for? e.g. `{rand.choice(humor)}`\n\n(_Psst:_ Say `cancel` to cancel the reminder.)")
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} Reminder cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                reminder = message.content
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name
        await ctx.send(f"{ctx.author.mention} When do you want to be reminded? e.g. `1 hour 30 minutes`\n\n(_Psst:_ You can specify the number of days, hours, and/or minutes. Say `cancel` to cancel the reminder.)")
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            message = await self.bot.wait_for("message", timeout=30.0, check=check)
            if message.content.lower() == "cancel":
                await ctx.send(f":x: {ctx.author.mention} Reminder cancelled.")
                usage.update(ctx)
                return ctx.command.name
            waittime = message.content
        except asyncio.TimeoutError:
            await ctx.send(f":x: {ctx.author.mention} Command timed out.")
            usage.update(ctx)
            return ctx.command.name
        times = lbutil.parse_time(waittime)
        elapsed_time = times["d"] * 24 * 60 + times["h"] * 60 + times["m"]
        if elapsed_time <= 0:
            try:
                elapsed_time = int(waittime)
            except ValueError:
                elapsed_time = 5
        print_time = lbutil.eng_time(60 * elapsed_time, seconds=False)
        timestamp = math.floor(time.time() / 60) + elapsed_time
        set_on = f"{datetime.now().replace(microsecond=0)} {time.tzname[0]}"
        set_for = f"{datetime.fromtimestamp(timestamp * 60).strftime('%Y-%m-%d %H:%M')} {time.tzname[0]}"
        with io.open("data/reminders.json") as f:
            reminders = json.load(f)
            reminders["reminders"].append(
                {
                    "timestamp": timestamp,
                    "author": ctx.author.id,
                    "time": print_time,
                    "message": reminder,
                    "set_on": set_on,
                    "set_for": set_for
                }
            )
            new_reminders = json.dumps(reminders, indent=4)
            with io.open("data/reminders.json", "w+", encoding="utf-8") as fo:
                fo.write(new_reminders)
        await ctx.send(f":reminder_ribbon: {ctx.author.mention} A reminder has been set for {print_time} from now ({set_for})!")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="reminders")
    async def cmd_reminders(self, ctx):
        with io.open("data/reminders.json") as f:
            reminders = json.load(f)["reminders"]
            my_reminders = []
            for reminder in reminders:
                if reminder["author"] == ctx.author.id:
                    my_reminders.append(reminder)
            if len(my_reminders) == 0:
                await ctx.send(f"{ctx.author.mention} You currently have no reminders set. Use `{ctx.prefix}remind` to set one, you forgetful bum.")
                usage.update(ctx)
                return ctx.command.name
            embeds = [discord.Embed(title=f"🎗️ Reminders for {ctx.author}")]
            count = 0
            for reminder in my_reminders:
                if count >= 25:
                    embeds.append(discord.Embed(title=f"🎗️ Reminders for {ctx.author}"))
                    count = 0
                embeds[len(embeds) - 1].add_field(name=f"Reminder for {reminder['set_for']}", value=reminder["message"])
                count += 1
            for i in range (0, len(embeds)):
                embeds[i].set_footer(text=f"Page {i + 1}")
            for e in embeds:
                await ctx.send(embed=e)
            usage.update(ctx)
            return ctx.command.name

def setup(bot):
    bot.add_cog(Utility(bot))
