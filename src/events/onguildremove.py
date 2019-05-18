import discord
from discord.ext import commands
import asyncio
import aiohttp
import socket

from utils import lbvars

class OnGuildRemove(commands.Cog):
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_remove(self,guild):
        """Runs whenver lmao-bot is removed from the server"""
        guild_count = lbvars.decrement_guild_count()
        lbvars.LOGGER.info("%s just REMOVED lmao-bot ;_;", guild.name)
        dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
        payload = {"server_count"  : len(self.bot.guilds), "shard_count": len(self.bot.shards)}
        async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
            async with aioclient.post(lbvars.dbl_url, data=payload, headers=lbvars.dbl_headers):
                await dbl_connector.close()
                await aioclient.close()

def setup(bot):
    bot.add_cog(OnGuildRemove(bot))