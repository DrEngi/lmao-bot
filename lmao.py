"Main entry for lmao-bot"

# Standard Python imports
import logging
import io
import time
from datetime import datetime
import socket
import os
import json

# Pip imports
import asyncio
import discord
from discord.ext import commands
import aiohttp

# First-party imports
from modules import dblpy
from modules import fun

from utils import lbvars
from utils import lbutil
from utils import dbl

print("lmao-bot is loading...")
print("All modules imported successfully.")

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def get_pre(bot, message):
    try:
        prefix = lbvars.get_prefix(message.guild.id)
    except discord.ext.commands.errors.CommandInvokeError:
        prefix = "lmao"
    prefixes = lbutil.get_permutations(prefix)
    return prefixes
bot = commands.Bot(command_prefix=get_pre, case_insensitive=True)
bot.remove_command("help")
def starts_with_prefix(message):
    prefixes = get_pre(bot, message)
    for prefix in prefixes:
        if message.content.startswith(prefix):
            return True
    return False

def load_extensions(bot):
    os.chdir("modules")
    if __name__ == "__main__":
        for path in os.listdir():
            if os.path.isfile(path):
                module = os.path.splitext(path)[0]
                if module != "__init__":
                    try:
                        bot.load_extension(f"modules.{module}")
                        print("{} sucessfully loaded.".format(module))
                    except Exception as e:
                        print("{} could not be loaded because {}.".format(module, e))
    os.chdir("..")
load_extensions(bot)

def get_all_commands():
    commands = []
    for command in bot.commands:
        commands.append(command.name)
        for alias in command.aliases:
            commands.append(alias)
    return commands

print("All extensions loaded.")

dblpy = bot.cogs.get("DBL")

with io.open("tokens/lmao-dev.txt", "r") as token:
    bot_token = (token.read()).strip()
with io.open("tokens/dbl.txt", "r") as token:
    dbl_token = (token.read()).strip()
dbl_url = "https://discordbots.org/api/bots/459432854821142529/stats"
dbl_headers = {"Authorization" : dbl_token}

bot_is_ready = False        # If bot is not ready, on_message event will not fire

async def check_reminders(late=False):
    with io.open("data/reminders.json") as f:
        reminders = json.load(f)
        for i in range(len(reminders["reminders"]) - 1, -1, -1):
            reminder = reminders["reminders"][i]
            if int(reminder["timestamp"]) <= round(time.time() / 60):
                late_msg = ""
                if late:
                    late_msg = "(If you are receiving this reminder late, the bot was likely offline when you should have received it.)"
                e = discord.Embed(title=f"🎗️ Reminder for {reminder['set_for']}", description=f"{reminder['message']}\n\n{late_msg}")
                e.set_footer(text=f"{reminder['time']} reminder set on {reminder['set_on']}.")
                try:
                    await bot.get_user(reminder["author"]).send(embed=e)
                except AttributeError:
                    print(f"Error in getting user {reminder['author']}")
                reminders["reminders"].pop(i)
        new_reminders = json.dumps(reminders, indent=4)
        with io.open("data/reminders.json", "w+", encoding="utf-8") as fo:
            fo.write(new_reminders)

@bot.event
async def on_ready():   # Prints ready message in terminal
    await dblpy.get_upvote_info()
    lbvars.reset_guild_count()
    print("Importing settings...")
    lbvars.import_settings()
    print("All settings successfully imported.")
    for guild in bot.guilds:
        lbvars.update_settings(guild.id, lbvars.GuildSettings(guild.id))
        guild_count = lbvars.increment_guild_count()
        print(str(datetime.now()) + " " + "{} initialized. Guild count: {}.".format(guild.name, guild_count))
    async def owner_has_voted():
        if (await dbl.has_voted(210220782012334081)):
            return "YES"
        return "NO"
    owner_voted = await owner_has_voted()
    print(f"Have you voted yet? {owner_voted}")
    print("Logged in as")
    print(bot.user.name)
    print(str(bot.user.id))
    print(str(datetime.now()))
    print("------")
    await bot.change_presence(activity=discord.Game(name="lmao help | in {} guilds | Firestar493#6963".format(len(bot.guilds))))
    lbvars.set_start_time(time.time())
    global bot_is_ready
    bot_is_ready = True
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.guilds)}
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()
    try:
        await check_reminders(late=True)
    except Exception as e:
        print(f"Error: {e}")
    await asyncio.sleep(60 - round(time.time()) % 60)
    while(True):
        try:
            await check_reminders()
        except Exception as e:
            print(f"Reminder check error: {e}")
        if not lbvars.custom_game:
            await bot.change_presence(activity=discord.Game(name="lmao help | in {} guilds | Firestar493#6963".format(len(bot.guilds))))
        await asyncio.sleep(60)

@bot.event
async def on_guild_join(guild):
    # lbvars.import_settings()
    lbvars.update_settings(guild.id, lbvars.GuildSettings(guild.id))
    guild_count = lbvars.increment_guild_count()
    print(str(datetime.now()) + " " + "{} initialized. Guild count: {}.".format(guild.name, guild_count))
    print(str(datetime.now()) + " " + guild.name + " just ADDED lmao-bot ^_^")
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.guilds)}
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()

@bot.event
async def on_guild_remove(guild):
    print(str(datetime.now()) + " " + guild.name + " just REMOVED lmao-bot ;_;")
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.guilds)}
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()

welcome = {
    463758816270483476: 469491274219782144, # lmao-bot Support
    407274897350328345: 472965450045718528, # Bot Testing Environment
    264445053596991498: 265156361791209475  # Discord Bot List
}

#Welcomes people in the lmao-bot support server
@bot.event
async def on_member_join(member):
    channel_id = welcome.get(member.guild.id, 0)
    if channel_id == 0:
        return
    mention = True
    if channel_id == 265156361791209475:
        mention = False
    channel = member.guild.get_channel(channel_id)
    await channel.trigger_typing()
    await fun.beautiful_welcome(member, channel, mention=mention)

#Bids people farewell in the lmao-bot support server
@bot.event
async def on_member_remove(member):
    channel_id = welcome.get(member.guild.id, 0)
    if channel_id == 0:
        return
    channel = member.guild.get_channel(channel_id)
    await channel.send(f"Good night, sweet {member}. You will be missed. :pensive:")

@bot.event
async def on_message(message):  # Event triggers when message is sent
    if not bot_is_ready:
        return

    # Prevent the bot from activating from other bots
    if message.author.bot:
        return

    guild = message.guild
    if guild is None:
        guild = message.channel
    guild_id = str(guild.id)

    prefix = lbvars.get_prefix(guild_id)
    msg_raw = message.content
    msg = msg_raw.lower()

    ctx = commands.Context(message=message, bot=bot, prefix=prefix)

    async def replace_ass():    # Sends the ass substitution message
        await bot.get_command("replaceass").invoke(ctx)
        lbvars.set_last_use_time(time.time())

    if message.guild is None:
        print(str(datetime.now()) + " DM from " + str(message.author) + ": " + message.content)
        if message.author.id == 309480972707954688:
            await message.channel.send("Hey, babe, what's up? :smirk:")
        if "help" in message.content:
            await bot.get_command("help").invoke(ctx)
        elif "lmao" in message.content or "lmfao" in message.content:
            await replace_ass()
        else:
            await bot.get_command("info").invoke(ctx)
        lbvars.set_last_use_time(time.time())
        return

    # If used by bot's creator, displays last time a lmao-bot command was used
    if message.author.id == 210220782012334081 and message.content.lower().strip() == "last command used":
        current_time = time.time()
        await message.channel.send(f"The last command was used {lbutil.eng_time(current_time - lbvars.get_last_use_time())} ago.")

    # COMMANDS
    if starts_with_prefix(message): # Bot reacts to command prefix call
        prefix = lbvars.get_prefix(guild_id)
        msg_no_prefix = message.content[len(prefix):].strip()
        words = msg_no_prefix.split()
        cmd_name = ""
        if len(words) > 0:
            cmd_name = words[0]

        # lbvars.import_settings()

        if cmd_name.lower() in get_all_commands():
            await bot.process_commands(message)
        else:
            try:
                await message.channel.send(lbvars.get_custom_cmd_list(message.guild.id)[cmd_name].strip())
            except KeyError:
                if "lmao" in message.content.lower() or "lmfao" in message.content.lower():
                    await replace_ass()

        if not lbvars.get_no_command_invoked():
            lbvars.set_last_use_time(time.time())
        lbvars.set_no_command_invoked(False)

        lbvars.export_settings(guild_id)

    elif msg == "lmao help":
        await message.channel.send(f"Type `{prefix} help` to see the help menu.")
    elif msg == "lmao prefix":
        await message.channel.send(f"My command prefix for {message.guild.name} is currently `{prefix}`.")

    # GENERIC REPLY
    elif ("lmao" in msg or "lmfao" in msg): #generic ass substitution
        await replace_ass()
        lbvars.export_settings(guild_id)

    if guild_id in ["345655060740440064", "407274897350328345"] and ("pollard" in msg or "buh-bye" in msg or "buhbye" in msg or "buh bye" in msg):
        emoji_list = bot.get_guild(345655060740440064).emojis
        for emoji in emoji_list:
            if emoji.name == "buhbye":
                buhbye = emoji
        try:
            await message.add_reaction(buhbye)
        except UnboundLocalError:
            pass
        except discord.errors.Forbidden:
            pass

bot.run(bot_token)
