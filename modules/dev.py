"""Developer Commands"""
import discord
from discord.ext import commands
import io
import json
import math
import asyncio
from utils import lbvars, usage, perms, lbutil
import time
import pandas as pd

class Dev:
    "Developer Commands"
    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot

    async def __local_check(self, ctx):
        is_dev = perms.is_lmao_developer(ctx.message)
        if not is_dev:
            await self.bot.get_command("replaceass").invoke(ctx)
        return is_dev

    @commands.command(name="getmarkdown", hidden=True)
    async def cmd_get_markdown(self, ctx, *, arg=""):
        await ctx.send(f"`{arg}`")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="getemoji", hidden=True)
    async def cmd_get_emoji(self, ctx, *, arg=""):
        emoji = lbutil.get_emoji(arg)
        if emoji is not None:
            id = lbutil.get_emoji_id(arg)
            await ctx.message.add_reaction(self.bot.get_emoji(id))
            await ctx.send(emoji)
        else:
            await ctx.send(f"Emoji {arg} not found.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="addemoji", hidden=True)
    async def cmd_add_emoji(self, ctx, *, arg=""):
        with io.open("data/emojis.json") as f:
            emojis = json.load(f)
        colon1 = arg.find(":")
        colon2 = colon1 + arg[colon1 + 1:].find(":") + 1
        if colon1 == -1 or colon2 == -1:
            await ctx.send(f"{arg} is an invalid emoji.")
            usage.update(ctx)
            return ctx.command.name
        name = arg[colon1 + 1:colon2].strip()
        emojis[name] = arg
        new_emojis = json.dumps(emojis, indent=4)
        with io.open("data/emojis.json", "w+") as f:
            f.write(new_emojis)
        await ctx.send(f":white_check_mark: `{name}` added as an emoji. {arg}")

    @commands.command(name="announce", hidden=True)
    async def cmd_announce(self, ctx, *, arg=""):
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
        lbvars.set_maintenance_time(arg)
        await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {lbvars.maintenance_time} | Firestar493#6963"))
        lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="changegame", hidden=True)
    async def cmd_change_game(self, ctx, *, arg=""):
        await self.bot.change_presence(activity=discord.Game(name=arg))
        lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displaymaintenance", hidden=True)
    async def cmd_display_maintenance(self, ctx):
        await self.bot.change_presence(activity=discord.Game(name=f"lmao help | Maint.: {lbvars.maintenance_time} | Firestar493#6963"))
        lbvars.custom_game = True
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="displayguildcount", aliases=["displayservercount"], hidden=True)
    async def cmd_display_guild_count(self, ctx):
        await self.bot.change_presence(activity=discord.Game(name=f"lmao help | {len(self.bot.guilds)} servers | Firestar493#6963"))
        lbvars.custom_game = False
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="showusage", hidden=True)
    async def cmd_show_usage(self, ctx, bars=15, width=6.4, height=4.8):
        with io.open("data/cmd_usage.json") as f:
            usage_data = json.load(f)
        commands = []
        uses = []
        max = 0
        for cmd, data in usage_data.items():
            if cmd == "replaceass" or cmd == "replace_ass":
                continue
            try:
                count = data["uses"]
                uses.append(count)
                commands.append(cmd)
                if count > max:
                    max = count
            except KeyError:
                continue
        for i in range(0, len(commands), bars):
            df = pd.DataFrame({"Command": commands[i:i+bars], "Uses": uses[i:i+bars]})
            ax = df.plot.bar(title="Command Usage for Lmao-Bot", x="Command", y="Uses", ylim=(0, max * 1.05), rot=45, figsize=(width, height))
            for p in ax.patches:
                ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
            fp = "management/usage.png"
            fig = ax.get_figure()
            fig.savefig(fp)
            await ctx.send(file=discord.File(fp))
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Dev(bot))
