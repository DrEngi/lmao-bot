import dbl
import discord
from discord.ext import commands

import aiohttp
import asyncio
import socket
import io

from utils import dbl as dblutils

class DBL:
    """Handles interactions with the discordbots.org API"""

    def __init__(self, bot):
        self.bot = bot
        self.token = dblutils.dbl_token #  set this to your DBL token
        self.dblpy = dbl.Client(self.bot, self.token, loop=bot.loop)
        # self.updating = bot.loop.create_task(self.update_stats())

    async def get_upvote_info(self):
        if self.bot.user.id != 459432854821142529:
            return {}
        upvotes = await self.dblpy.get_upvote_info(days=1)
        #print(upvotes)
        return upvotes

    # async def update_stats(self):
    #     """This function runs every 30 minutes to automatically update your server count"""
    #     await self.bot.is_ready()
    #     while not bot.is_closed():
    #         try:
    #             await self.dblpy.post_server_count()
    #         except Exception as e:
    #             print("Server count post failed.")
    #         await asyncio.sleep(1800)

def setup(bot):
    bot.add_cog(DBL(bot))
