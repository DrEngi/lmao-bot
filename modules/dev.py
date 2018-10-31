import discord
from discord.ext import commands
from utils import lbvars, perms, usage

class Dev:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="d!serverusage", aliases=[])
    async def cmd_d_serverUsage(self, ctx): # Get latest commands executed by server
        guild_id = ctx.guild.id
        if perms.is_lmao_developer(ctx.message):
            await ctx.send(ctx.author.mention + " Not implemented yet.")
        else:
            await ctx.send(ctx.author.mention + " You do not have the permission to change the ass replacement chance. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name