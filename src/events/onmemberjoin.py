import discord
from discord.ext import commands
import asyncio

from modules import fun
from utils import lbvars
class OnMemberJoin:
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot
    
    async def on_member_join(self, member):
        """Runs welcome message whenever a member joins"""
        channel_id = lbvars.welcome.get(member.guild.id, 0)
        if channel_id == 0:
            return
        mention = True
        if channel_id == 265156361791209475:
            mention = False
        channel = member.guild.get_channel(channel_id)
        await channel.trigger_typing()
        fun_cog = self.bot.get_cog("Fun")
        await fun.beautiful_welcome(member, channel, mention=mention)

def setup(bot):
    bot.add_cog(OnMemberJoin(bot))