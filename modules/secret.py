"Developer Commands and such"
import discord
from discord.ext import commands
import io
import asyncio
from utils import lbvars, usage, perms, lbutil
import time

class Secret:
    "Developer Commands"
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="announce", hidden=True)
    async def cmd_announce(self, ctx, *, arg=""):
        if perms.is_lmao_developer(ctx.message):
            for guild in self.bot.guilds:
                for channel in guild.text_channels:
                    try:
                        if channel.permissions_for(guild.me).send_messages:
                            with io.open("management/announcement_finished.txt", "a") as f:
                                f.write(f"{guild.name} ({guild.id})")
                            await channel.send(arg)
                            break
                    except AttributeError:
                        pass
                    except discord.errors.Forbidden:
                        pass
                await asyncio.sleep(10)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="changemaintenance", hidden=True)
    async def cmd_change_maintenance(self, ctx, *, arg=""):
        if perms.is_lmao_developer(ctx.message):
            lbvars.set_maintenance_time(arg)
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {lbvars.maintenance_time} | Firestar493#6963"))
            lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="changegame", hidden=True)
    async def cmd_change_game(self, ctx, *, arg=""):
        if perms.is_lmao_developer(ctx.message):
            await self.bot.change_presence(activity=discord.Game(name=arg))
            lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displaymaintenance", hidden=True)
    async def cmd_display_maintenance(self, ctx):
        if perms.is_lmao_developer(ctx.message):
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {lbvars.maintenance_time} | Firestar493#6963"))
            lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displayguildcount", hidden=True)
    async def cmd_display_guild_count(self, ctx):
        if perms.is_lmao_developer(ctx.message):
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | in {len(self.bot.guilds)} guilds | Firestar493#6963"))
            lbvars.custom_game = False
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Secret(bot))
