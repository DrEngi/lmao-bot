import discord
from discord.ext import commands
import io
import json
import asyncio
from utils import lbvars, perms, usage

class Settings:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="toggle", aliases=["toggleass", "asstoggle", "on", "off", "lotto"])
    async def cmd_toggle(self, ctx, arg=""): # Toggle whether automatic ass substitution happens or not
        guild_id = ctx.guild.id
        if perms.is_lmao_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages:
            valid_shortcuts = ["on", "off", "lotto"]
            new_chance = arg
            if new_chance == "" and ctx.invoked_with not in valid_shortcuts:
                await ctx.send(f"{ctx.author.mention} My current ass replacement chance for {ctx.guild.name} is `{lbvars.get_replace_ass_chance(guild_id)}%`. What should I change it to?\n\n(Note: Say `cancel` to cancel this change.)")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} Ass replacement chance change cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    new_chance = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            valid_chance = True
            chance = lbvars.get_replace_ass_chance(guild_id)
            try:
                chance = int(new_chance.replace("%", ""))
                if chance < 0 or chance > 100:
                    valid_chance = False
            except ValueError:
                if new_chance == "off" or ctx.invoked_with == "off":
                    chance = 0
                elif new_chance == "on" or ctx.invoked_with == "on":
                    chance = 100
                elif new_chance == "lotto" or ctx.invoked_with == "lotto":
                    chance = 1
                else:
                    valid_chance = False
            if valid_chance:
                after_msg = ""
                if chance <= 50:
                    after_msg = "Tread carefully, and hold onto your buns."
                else:
                    after_msg = "Don't do anything reckless; you'll be fine."
                lbvars.set_replace_ass_chance(guild_id, chance)
                await ctx.send(f"You have changed the automatic ass replacement chance for {ctx.guild.name} to `{chance}%`. {after_msg}")
            else:
                await ctx.send(f"{ctx.author.mention} You must include an integer after toggleass from 0 to 100. This is the chance (in %) of automatic ass replacement.")
        else:
            await ctx.send(ctx.author.mention + " You do not have the permission to change the ass replacement chance. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="react", aliases=["togglereact", "reacttoggle"])
    async def cmd_react(self, ctx, arg=""):
        guild_id = ctx.guild.id
        if perms.is_lmao_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages:
            new_chance = arg
            if new_chance == "":
                await ctx.send(f"{ctx.author.mention} My current reaction chance for {ctx.guild.name} is `{lbvars.get_react_chance(guild_id)}%`. What should I change it to?\n\n(Note: Say `cancel` to cancel this change.)")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} Reaction chance change cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    new_chance = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            valid_chance = True
            chance = lbvars.get_react_chance(guild_id)
            try:
                chance = int(new_chance.replace("%", ""))
                if chance < 0 or chance > 100:
                    valid_chance = False
            except ValueError:
                if new_chance == "off":
                    chance = 0
                elif new_chance == "on":
                    chance = 100
                else:
                    valid_chance = False
            if valid_chance:
                after_msg = ""
                if chance == 0:
                    after_msg = "Looks like the Fine Bros found us. :pensive:"
                else:
                    after_msg = "Watch out for the Fine Bros. :eyes:"
                lbvars.set_react_chance(guild_id, chance)
                await ctx.send(f"You have changed the automatic emoji reaction chance for {ctx.guild.name} to `{chance}%`. {after_msg}")
            else:
                await ctx.send(r'You must include an integer after `react` from 0 to 100. This is the chance (in %) of automatic emoji reactions.')
        else:
            await ctx.send(ctx.author.mention + " You do not have the permission to change the reaction chance. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="chance")
    async def cmd_chance(self, ctx):
        guild_id = ctx.guild.id
        e = discord.Embed(title=f"{ctx.guild.name} Chance Settings")
        e.add_field(name="Ass replacement", value=f"{lbvars.get_replace_ass_chance(guild_id)}%")
        e.add_field(name="Ass reaction", value=f"{lbvars.get_react_chance(guild_id)}%")
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="count")
    async def cmd_count(self, ctx):  # Counts the number of times someone says lmao
        with io.open("data/user_data.json") as f:
            lmao_count_data = json.load(f)
            try:
                await ctx.send(ctx.author.mention + " You have laughed your ass off {} times.".format(lmao_count_data[str(ctx.author.id)]["lmao_count"]))
            except KeyError:
                await ctx.send(ctx.author.mention + " You have yet to laugh your ass off.")
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Settings(bot))
