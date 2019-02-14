import discord
from discord.ext import commands
import asyncio
import aiohttp
import socket

import time
from datetime import datetime, timedelta

from utils import lbvars, dbl
from modules import dblpy
import json, io

class OnReady:
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot
        self.dblpy = bot.cogs.get("DBL")

    async def check_reminders(self, late=False):
        """Check all reminders"""
        with io.open("../data/reminders.json") as f:
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
                        await self.bot.get_user(reminder["author"]).send(embed=e)
                    except AttributeError:
                        print(f"Error in getting user {reminder['author']}")
                    reminders["reminders"].pop(i)
            new_reminders = json.dumps(reminders, indent=4)
            with io.open("../data/reminders.json", "w+", encoding="utf-8") as fo:
                fo.write(new_reminders)

    async def check_dc(self):
        keys_to_delete = []
        for guild_id, dc_time in lbvars.dc_time.items():
            if round((datetime.now() - dc_time).total_seconds()) >= 0:
                try:
                    channel = self.bot.get_cog("Music").players[guild_id]._channel
                    await channel.send("⏰ The voice channel has been inactive for 15 minutes. Now leaving...")
                    self.bot.get_cog("Music").players.pop(guild_id, 0)
                    await self.bot.get_guild(guild_id).voice_client.disconnect()
                    # player.destroy(player._guild)
                    # await player.send_np(finished=True, timeout=True)
                    # await BOT.get_guild(guild_id).voice_client.disconnect()
                except KeyError:
                    pass
                keys_to_delete.append(guild_id)
        for key in keys_to_delete:
            del lbvars.dc_time[key]
    
    async def on_ready(self):
        """Prints ready message in terminal""" 
        lbvars.reset_guild_count()
        for guild in self.bot.guilds:
            # lbvars.update_settings(guild.id, lbvars.GuildSettings(guild.id))
            new_guild = lbvars.init_settings(guild.id)
            guild_count = lbvars.increment_guild_count()
            keyword = "OLD: "
            if new_guild:
                "NEW: "
            lbvars.LOGGER.info(str("#{}. {}{}.".format(guild_count, keyword, guild.name)))
        voted = await self.dblpy.get_upvote_info()
        lbvars.LOGGER.info(f"{len(voted)} users have voted.")
        lbvars.LOGGER.info("Logged in as")
        lbvars.LOGGER.info(self.bot.user.name)
        lbvars.LOGGER.info(str(self.bot.user.id))
        lbvars.LOGGER.info(str(datetime.now()))
        lbvars.LOGGER.info("------")
        await self.bot.change_presence(activity=discord.Game(name=f"lmao help | {len(self.bot.guilds)} servers"))
        lbvars.set_start_time(time.time())
        lbvars.bot_is_ready = True
        dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
        payload = {"server_count"  : len(self.bot.guilds), "shard_count": len(self.bot.shards)}
        async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
            async with aioclient.post(lbvars.dbl_url, data=payload, headers=lbvars.dbl_headers):
                dbl_connector.close()
                await aioclient.close()
        try:
            await self.check_reminders(late=True)
        except Exception as Ex:
            lbvars.LOGGER.warning("Error: %s", Ex)
        await asyncio.sleep(60 - round(time.time()) % 60)
        while(True):
            try:
                await self.check_reminders()
            except Exception as Ex:
                lbvars.LOGGER.warning("Reminder check error: %s", Ex)
            try:
                await self.check_dc()
            except Exception as Ex:
                lbvars.LOGGER.warning("Disconnection check error: %s", Ex)
            if not lbvars.custom_game:
                await self.bot.change_presence(activity=discord.Game(name=f"lmao help | {len(self.bot.guilds)} servers"))
            await asyncio.sleep(60)

def setup(bot):
    bot.add_cog(OnReady(bot))