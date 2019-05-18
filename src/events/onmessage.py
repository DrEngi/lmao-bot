import discord
from discord.ext import commands
import asyncio

import time, random
from utils import lbvars, lbutil, perms

class OnMessage(commands.Cog):
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot
        print("initting onmessage")

    def get_pre(self, bot, message):
        "Gets the prefix for the guild the message was sent it, otherwise returns lmao"
        try:
            prefix = lbvars.get_prefix(message.guild.id)
        except discord.ext.commands.errors.CommandInvokeError:
            prefix = "lmao"
        prefixes = lbutil.get_permutations(prefix) # Returns a list of strings that are prefixes
        return prefixes

    def get_mentioned_or_pre(self, bot, message):
        prefixes = self.get_pre(bot, message)
        return commands.when_mentioned_or(*prefixes)(bot, message)
    
    def starts_with_prefix(self, message):
        "Determines whether or not the current prefix was used in the message."
        if message.content.startswith(self.bot.user.mention):
            return True
        prefixes = self.get_pre(self.bot, message)
        for prefix in prefixes:
            if message.content.startswith(prefix):
                return True
        return False

    def get_all_commands(self):
        """Returns all commands in the bot set by Discord.ext"""
        commands = []
        for command in self.bot.commands:
            commands.append(command.name)
            for alias in command.aliases:
                commands.append(alias)
        return commands
    
    @commands.Cog.listener()
    async def on_message(self, message):  # Event triggers when message is sent
        """Runs whenever a message is sent"""
        if not lbvars.bot_is_ready:
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

        ctx = commands.Context(message=message, bot=self.bot, prefix=prefix)

        async def replace_ass():    # Sends the ass substitution message
            await self.bot.get_command("replaceass").invoke(ctx)
            lbvars.set_last_use_time(time.time())

        if message.guild is None:
            lbvars.LOGGER.info("DM from %s: %s", message.author, message.content)
            if message.author.id == 309480972707954688:
                await message.channel.send("Hey, babe, what's up? :smirk:")
            if "help" in message.content:
                await self.bot.get_command("help").invoke(ctx)
            elif "lmao" in message.content or "lmfao" in message.content:
                await replace_ass()
            else:
                await self.bot.get_command("info").invoke(ctx)
            lbvars.set_last_use_time(time.time())
            return

        # If used by bot's creator, displays last time a lmao-bot command was used
        # DEV NOTE: This is expensive and there are better ways to handle this then running an if statement for every message.
        # if perms.is_lmao_developer(ctx.message) and message.content.lower().strip() == "last command used":
        #     current_time = time.time()
        #     await message.channel.send(f"The last command was used {lbutil.eng_time(current_time - lbvars.get_last_use_time())} ago.")

        #COMMANDS
        if self.starts_with_prefix(message): # Bot reacts to command prefix call
            if message.content.startswith(self.bot.user.mention):
                prefix = self.bot.user.mention
            else:
                prefix = lbvars.get_prefix(guild_id)
            msg_no_prefix = message.content[len(prefix):].strip()
            words = msg_no_prefix.split()
            cmd_name = ""
            if len(words) > 0:
                cmd_name = words[0]

            # lbvars.import_settings()

            if cmd_name.lower() in self.get_all_commands():
                await self.bot.process_commands(message)
            else:
                try:
                    await message.channel.send(perms.clean_everyone(ctx, lbvars.get_custom_cmd_list(message.guild.id)[cmd_name].strip()))
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

        #FILTERS
        else:
            filters = lbvars.get_filter_list(guild_id)
            for key, value in filters.items():
                flags = value["flags"]
                if "chance" in flags:
                    chance = lbutil.parse_chance(flags)
                    x = random.randint(1, 100)
                    if x > chance:
                        continue
                needle = key.lower()
                haystack = ctx.message.content.lower()
                if "casesensitive" in flags:
                    needle = key
                    haystack = ctx.message.content
                if "wholeword" in flags:
                    haystack = haystack.split()
                contains_key = needle in haystack
                if contains_key:
                    mention = f"{message.author.mention} "
                    if "nomention" in flags:
                        mention = ""
                    await ctx.send(perms.clean_everyone(ctx, f"{mention}{value['message']}"))
            lbvars.export_settings(guild_id)

        if guild_id in ["345655060740440064", "407274897350328345"] and ("pollard" in msg or "buh-bye" in msg or "buhbye" in msg or "buh bye" in msg):
            emoji_list = self.bot.get_guild(345655060740440064).emojis
            for emoji in emoji_list:
                if emoji.name == "buhbye":
                    buhbye = emoji
            try:
                await message.add_reaction(buhbye)
            except UnboundLocalError:
                pass
            except discord.errors.Forbidden:
                pass

def setup(bot):
    bot.add_cog(OnMessage(bot))