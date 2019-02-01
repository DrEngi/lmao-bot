import discord
from discord.ext import commands
from utils import lbvars, usage, perms
import asyncio

class Custom:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add", aliases=["addcmd"])
    async def cmd_add(self, ctx, pname="", *, parg=""):   #adds custom command
        if perms.is_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages:
            name = pname
            arg = parg
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            if name == "":
                await ctx.send(f"{ctx.author.mention} What should the command name be?\n\n(Note: the command name may not contain spaces or line breaks. Type `cancel` to cancel the new command.)")
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} New command cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    name = message.content.strip().split()[0].strip()
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            if name in lbvars.get_custom_cmd_list(ctx.guild.id):
                await ctx.send(f"{ctx.author.mention} `{name}` already exists as a command.")
                usage.update(ctx)
                return ctx.command.name
            if arg == "":
                await ctx.send(f"{ctx.author.mention} What should `{ctx.prefix}{name}` say when used?\n\n(Say `cancel` to cancel the new command.)")
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} New command cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    arg = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            lbvars.add_custom_cmd(ctx.guild.id, name, arg)
            await ctx.send(f"`{name}` added as a custom command.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to add custom commands. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="edit", aliases=["editcmd"])
    async def cmd_edit(self, ctx, pname="", *, parg=""):  #edits existing custom command
        if perms.is_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages:
            name = pname
            arg = parg
            def check(message):
                return message.author == ctx.author and message.channel == ctx.channel
            if name == "":
                await ctx.send(f"{ctx.author.mention} Which command do you want to edit?\n\n(Say `cancel` to cancel the command edit.)")
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} Command edit cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    name = message.content.strip().split()[0].strip()
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            if name not in lbvars.get_custom_cmd_list(ctx.guild.id):
                await ctx.send(f"{ctx.author.mention} `{name}` does not exist as a command.")
                usage.update(ctx)
                return ctx.command.name
            if arg == "":
                await ctx.send(f"{ctx.author.mention} What should `{ctx.prefix}{name}` say when used?\n\n(Say `cancel` to cancel the command edit.)")
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} Command edit cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    arg = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            lbvars.add_custom_cmd(ctx.guild.id, name, arg)
            await ctx.send(f"`{name}` custom command updated.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to edit custom commands. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="delete", aliases=["del", "delcmd", "deletecmd"])
    async def cmd_delete(self, ctx, arg=""):    #deletes existing custom command
        if perms.is_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages:
            name = arg
            if name == "":
                await ctx.send(f"{ctx.author.mention} Which command would you like to delete?\n\n(Type `cancel` to cancel deleting a command.)")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.bot.wait_for("message", timeout=10.0, check=check)
                    if message.content.lower() == "cancel":
                        await ctx.send(f":x: {ctx.author.mention} Deletion cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                    name = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            if name in lbvars.get_custom_cmd_list(ctx.guild.id):
                deleted_cmd_text = lbvars.get_custom_cmd_list(ctx.guild.id)[name]
                lbvars.delete_custom_cmd(ctx.guild.id, name)
                await ctx.send(f"`{name}` custom command deleted. It originally printed:")
                await ctx.send(deleted_cmd_text)
            else:
                await ctx.send(f"`{name}` does not exist as a command.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to delete custom commands. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="list", aliases=["cmdlist", "listcmd"])
    async def cmd_list(self, ctx):  # lists all custom commands
        title = f"Custom Commands for {ctx.guild.name}"
        embeds = [discord.Embed(title=title)]
        count = 0
        for name, value in lbvars.get_custom_cmd_list(ctx.guild.id).items():
            if count >= 20:
                embeds.append(discord.Embed(title=title))
                count = 0
            v = value
            if len(v) > 256:
                v = value[:253] + "..."
            embeds[len(embeds) - 1].add_field(name=name, value=v)
            count += 1
        for i in range(0, len(embeds)):
            embeds[i].set_footer(text=f"Page {i + 1}")
        for e in embeds:
            await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Custom(bot))
