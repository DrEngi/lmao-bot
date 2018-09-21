import discord
from discord.ext import commands
import random
import json
import io
from utils import vars, usage

class Peach:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="replaceass", aliases=["peach"], hidden=True)
    async def replace_ass(self, ctx):    # Sends the ass substitution message
        with io.open("data/user_data.json") as f:
            lmao_count_data = json.load(f)
            try:
                lmao_count_data[str(ctx.author.id)]["lmao_count"] += 1
            except KeyError:
                lmao_count_data[str(ctx.author.id)] = {"lmao_count": 1}
            lmao_count_data[str(ctx.author.id)]["username"] = str(ctx.author)
            new_user_data = json.dumps(lmao_count_data, indent=4)
            with io.open("data/user_data.json", "w+", encoding="utf-8") as fo:
                fo.write(new_user_data)
        x = random.randint(1, 100)
        if ctx.guild == None or x <= vars.get_react_chance(ctx.guild.id):
            try:
                await ctx.message.add_reaction('🍑')
            except discord.errors.Forbidden:
                pass
        y = random.randint(1, 100)
        if ctx.guild == None or y <= vars.get_replace_ass_chance(ctx.guild.id):
            try:
                await ctx.send(f"{ctx.author.mention} {vars.replace_ass_msg}")
            except discord.errors.Forbidden:
                pass
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Peach(bot))
