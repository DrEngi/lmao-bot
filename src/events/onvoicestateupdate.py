import discord
from discord.ext import commands
import asyncio

import time
from datetime import datetime, timedelta

from utils import lbvars

class OnVoiceStateUpdate:
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    async def on_voice_state_update(self, member, before, after):
        if member.guild.voice_client is None or not member.guild.voice_client.is_connected():
            return
        channel = member.guild.voice_client.channel # Gets the voice_client for the bot in this guild
        active = False
        for member in channel.members:
            if not member.bot:
                active = True
                break
        if active:
            lbvars.dc_time.pop(member.guild.id, 0)
        if not active:
            now = datetime.now()
            later = now + timedelta(minutes=15)
            if member.guild.id not in lbvars.dc_time:
                lbvars.dc_time[member.guild.id] = later

def setup(bot):
    bot.add_cog(OnVoiceStateUpdate(bot))