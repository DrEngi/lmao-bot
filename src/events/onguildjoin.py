import discord
from discord.ext import commands
import asyncio
import aiohttp
import socket

from utils import lbvars

class OnGuildJoin:
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        """Runs whenever lmao-bot joins a new server"""
        # lbvars.import_settings()d
        lbvars.update_settings(guild.id, lbvars.GuildSettings(guild.id))
        guild_count = lbvars.increment_guild_count()
        lbvars.LOGGER.info("#%s. %s initialized.", guild_count, guild.name)
        dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
        payload = {"server_count"  : len(self.bot.guilds), "shard_count": len(self.bot.shards)}
        async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
            async with aioclient.post(lbvars.dbl_url, data=payload, headers=lbvars.dbl_headers):
                dbl_connector.close()
                await aioclient.close()

def setup(bot):
    bot.add_cog(OnGuildJoin(bot))