"""Main entry for lmao-bot"""
# TODO: Use docstrings to clean up help menu

# Standard Python imports
import logging
import io
import inspect
import time
from datetime import datetime, timedelta
import socket
import os
import json
import random

# Pip imports
import asyncio
import discord
from discord.ext import commands
import aiohttp

# First-party imports
from modules import dblpy, fun
from utils import lbvars, lbutil, dbl, perms

def get_pre(bot, message):
    "Gets the prefix for the guild the message was sent it, otherwise returns lmao"
    try:
        prefix = lbvars.get_prefix(message.guild.id)
    except discord.ext.commands.errors.CommandInvokeError:
        prefix = "lmao"
    prefixes = lbutil.get_permutations(prefix) # Returns a list of strings that are prefixes
    return prefixes

def get_mentioned_or_pre(bot, message):
    prefixes = get_pre(bot, message)
    return commands.when_mentioned_or(*prefixes)(bot, message)


# Renames the previous log file so there is a continuous record of log files
try:
    os.rename("logs/lmao.log", f"logs/lmao-{time.time()}.log")
except FileNotFoundError:
    pass

with io.open("../tokens/lavalink.txt", "r") as lavalink:
    lbvars.lavalinkpass = (lavalink.read()).strip()

#Sets up logging here so we don't have to shoot ourselves
lbvars.LOGGER = logging.getLogger('discord')
lbvars.LOGGER.setLevel(logging.INFO)
FORMATTER = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
FILEHANDLER = logging.FileHandler(filename='logs/lmao.log', encoding='utf-8', mode='w')
FILEHANDLER.setFormatter(FORMATTER)
STREAMHANDLER = logging.StreamHandler()
STREAMHANDLER.setFormatter(FORMATTER)
lbvars.LOGGER.addHandler(STREAMHANDLER)
lbvars.LOGGER.addHandler(FILEHANDLER)

lbvars.LOGGER.info("lmao-bot is loading...")

BOT = commands.AutoShardedBot(command_prefix=get_mentioned_or_pre, case_insensitive=True)
BOT.remove_command("help")

def load_extensions(bot):
    """Loads all extensions found in the modules folder."""
    os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "/modules")
    if __name__ == "__main__":
        for path in os.listdir():
            if os.path.isfile(path):
                module = os.path.splitext(path)[0]
                if module != "__init__":
                    try:
                        bot.load_extension(f"modules.{module}")
                        lbvars.LOGGER.info("%s sucessfully loaded.", module)
                    except Exception as Ex:
                        lbvars.LOGGER.info("%s could not be loaded because %s.", module, Ex)
    os.chdir("..")

load_extensions(BOT)
BOT.load_extension("events.onmemberjoin")
BOT.load_extension("events.onguildjoin")
BOT.load_extension("events.onmemberremove")
BOT.load_extension("events.onguildremove")
BOT.load_extension("events.onready")
BOT.load_extension("events.onmessage")
#BOT.load_extension("events.onvoicestateupdate") commented out, not sure if required by lavalink

lbvars.LOGGER.info("All extensions loaded.")

with io.open("../tokens/token.txt", "r") as token:
    bot_token = (token.read()).strip()
with io.open("../tokens/dbl.txt", "r") as token:
    dbl_token = (token.read()).strip()
lbvars.dbl_url = "https://discordbots.org/api/bots/459432854821142529/stats"
lbvars.dbl_headers = {"Authorization" : dbl_token}

lbvars.LOGGER.info("Importing settings...")
lbvars.import_settings()
lbvars.LOGGER.info("All settings successfully imported.")

@BOT.event
async def on_message(message):
    "disables default onMessage since we handle it elsewhere"
    #this is hacky I know but it's required

BOT.run(bot_token)
