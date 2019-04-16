import discord
from discord.ext import commands
import asyncio

from utils import lbvars

class OnMemberRemove(commands.Cog):
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        """Bids people farewell in the lmao-bot support server"""
        
        channel_id = lbvars.welcome.get(member.guild.id, 0)
        if channel_id == 0:
            return
        channel = member.guild.get_channel(channel_id)
        await channel.send(f"Goodbye, {member}. You will be missed. :pensive:")

def setup(bot):
    bot.add_cog(OnMemberRemove(bot))