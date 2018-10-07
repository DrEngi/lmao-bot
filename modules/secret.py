import discord
from discord.ext import commands
import io
import asyncio
from utils import vars, usage

class Secret:

    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="announce", hidden=True)
    async def cmd_announce(self, ctx, *, arg=""):
        if ctx.author.id == 210220782012334081:
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
        else:
            await replace_ass()
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="changemaintenance", hidden=True)
    async def cmd_change_maintenance(self, ctx, *, arg=""):
        if ctx.author.id == 210220782012334081:
            vars.set_maintenance_time(arg)
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {vars.maintenance_time} | Firestar493#6963"))
            vars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="changegame", hidden=True)
    async def cmd_change_game(self, ctx, *, arg=""):
        if ctx.author.id == 210220782012334081:
            await self.bot.change_presence(activity=discord.Game(name=arg))
            vars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displaymaintenance", hidden=True)
    async def cmd_display_maintenance(self, ctx):
        if ctx.author.id == 210220782012334081:
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {vars.maintenance_time} | Firestar493#6963"))
            vars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displayguildcount", hidden=True)
    async def cmd_display_guild_count(self, ctx):
        if ctx.author.id == 210220782012334081:
            await self.bot.change_presence(activity=discord.Game(name=f"lmao help | in {len(self.bot.guilds)} guilds | Firestar493#6963"))
            vars.custom_game = False
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Secret(bot))
