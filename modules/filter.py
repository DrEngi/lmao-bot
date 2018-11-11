import discord
from discord.ext import commands
import json
import io
import asyncio
from utils import lbvars, usage, perms

class Filter:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    async def can_edit_filters(ctx):
        can_edit = perms.is_lmao_admin(ctx.message) or perms.get_perms(ctx.message).manage_messages
        if not can_edit:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to edit custom filters. Ask a guild administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
        return can_edit

    @commands.group(invoke_without_command=True, name="filter", aliases=["filters", "censor", "censors"])
    async def cmd_filter(self, ctx):
        """Guilds can set their own custom filters."""

        ### TODO: ###
        # Make this actual code that deals with filters.
        # Add a command which adds a filter + message to respond to filter.
        # Add a command which edits filters.
        # Add a command which removes filters.
        # Add a command to view all filters.
        # Potentially add configurations? e.g. mentions user, case sensitivity, chance, etc.

        with io.open("data/filters.json") as f:
            filter_data = json.load(f)
            if str(ctx.guild.id) not in filter_data or len(filter_data[str(ctx.guild.id)]) == 0:
                await ctx.send(f"{ctx.author.mention} Your guild currently has no custom filters set. Add some with `{ctx.prefix}filter add`!")
                usage.update(ctx)
                return ctx.command.name
            filters = filter_data[str(ctx.guild.id)]
        title = f"Custom filters for {ctx.guild.name}"
        desc = "Change filters with `{0} add`, `{0} edit`, `{0} flags`, and `{0} remove`.".format(f"{ctx.prefix}filter")
        count = 0
        page = 1
        e = discord.Embed(title=title, description=desc)
        for name, value in filters.items():
            filter_message = value["message"]
            flags = value["flags"].strip()
            if flags == "":
                flags = "none"
            flags = f" (flags: {flags})"
            if count == 25:
                e.set_footer(text=f"Page {page}")
                await ctx.send(embed=e)
                e = discord.Embed(title=title, description=desc)
                count = 0
                page += 1
            e.add_field(name=f"{name}{flags}", value=filter_message[:100])
            count += 1
        e.set_footer(text=f"Page {page}")
        await ctx.send(embed=e)

        usage.update(ctx)
        return ctx.command.name

    @cmd_filter.command(name="add")
    @commands.check(can_edit_filters)
    async def cmd_filter_add(self, ctx, *, arg=""):
        #TODO: Check if filter already exists
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        filter = arg.strip()
        if filter == "":
            await ctx.send(f"{ctx.author.mention} What word or phrase should be filtered?\n\n(Type `cancel` to cancel the new filter.)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} New filter cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                filter = message.content.strip()
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name
        if filter in lbvars.get_filter_list(ctx.guild.id):
            await ctx.send(f"{ctx.author.mention} `{filter}` already exists as a filter. Try editing it with `{ctx.prefix}filter edit`.")
            usage.update(ctx)
            return ctx.command.name
        await ctx.send(f"{ctx.author.mention} What should lmao-bot say when a message contains `{filter}`?\n\n(Type `cancel` to cancel the new filter.)")
        try:
            message = await self.bot.wait_for("message", timeout=30.0, check=check)
            if message.content.lower() == "cancel":
                await ctx.send(f":x: {ctx.author.mention} New filter cancelled.")
                usage.update(ctx)
                return ctx.command.name
            filter_message = message.content.strip()
        except asyncio.TimeoutError:
            await ctx.send(f":x: {ctx.author.mention} Command timed out.")
            usage.update(ctx)
            return ctx.command.name
        lbvars.add_filter(ctx.guild.id, filter, filter_message, "none")
        e = discord.Embed(title=f"✅ New filter added for {filter}", description=filter_message)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @cmd_filter.command(name="edit", aliases=["change", "update"])
    @commands.check(can_edit_filters)
    async def cmd_filter_edit(self, ctx, *, arg=""):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        filter = arg.strip()
        if filter == "":
            await ctx.send(f"{ctx.author.mention} Which word or phrase filter do you want to edit?\n\n(Type `cancel` to cancel the filter edit.)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} Filter edit cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                filter = message.content.strip()
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name
        filter_list = lbvars.get_filter_list(ctx.guild.id)
        if filter not in filter_list:
            await ctx.send(f"{ctx.author.mention} `{filter}` does not exist as a filter. Try adding it with `{ctx.prefix}filter add`.")
            usage.update(ctx)
            return ctx.command.name
        flags = filter_list[filter]["flags"]
        await ctx.send(f"{ctx.author.mention} What should lmao-bot say instead when a message contains `{filter}`?\n\n(Type `cancel` to cancel the filter edit.)")
        try:
            message = await self.bot.wait_for("message", timeout=30.0, check=check)
            if message.content.lower() == "cancel":
                await ctx.send(f":x: {ctx.author.mention} Filter edit cancelled.")
                usage.update(ctx)
                return ctx.command.name
            filter_message = message.content.strip()
        except asyncio.TimeoutError:
            await ctx.send(f":x: {ctx.author.mention} Command timed out.")
            usage.update(ctx)
            return ctx.command.name
        lbvars.add_filter(ctx.guild.id, filter, filter_message, flags)
        e = discord.Embed(title=f"✅ Filter for {filter} updated", description=filter_message)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @cmd_filter.command(name="flags", aliases=["config", "configure", "settings"])
    @commands.check(can_edit_filters)
    async def cmd_filter_config(self, ctx, *, arg=""):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        filter = arg.strip()
        if filter == "":
            await ctx.send(f"{ctx.author.mention} Which word or phrase filter do you want to change the flags of?\n\n(Type `cancel` to cancel the filter configuration.)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} Filter configuration cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                filter = message.content.strip()
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name
        filter_list = lbvars.get_filter_list(ctx.guild.id)
        if filter not in filter_list:
            await ctx.send(f"{ctx.author.mention} `{filter}` does not exist as a filter. Try adding it with `{ctx.prefix}filter add`.")
            usage.update(ctx)
            return ctx.command.name
        filter_message = filter_list[filter]["message"]
        flags = filter_list[filter]["flags"]
        await ctx.send(f"{ctx.author.mention} What flags should lmao-bot have for the `{filter}` filter?\n\n" \
            f"**Current flags**: `{flags}`\n\n" \
            f"**Possible flags**: `none` (no flags), `nomention` (filter does not mention user), `casesensitive` (filter is case-sensitive)\n\n" \
            "(Tip: You can include multiple flags if desired. Type `cancel` to cancel the filter configuration.)")
        try:
            message = await self.bot.wait_for("message", timeout=30.0, check=check)
            if message.content.lower() == "cancel":
                await ctx.send(f":x: {ctx.author.mention} Filter configuration cancelled.")
                usage.update(ctx)
                return ctx.command.name
            flag_message = message.content.strip()
        except asyncio.TimeoutError:
            await ctx.send(f":x: {ctx.author.mention} Command timed out.")
            usage.update(ctx)
            return ctx.command.name
        viable_flags = ["nomention", "casesensitive"]
        flags = ""
        for flag in viable_flags:
            if flag in flag_message:
                flags+= f"{flag} "
        flags = flags.strip()
        if flags == "":
            flags = "none"
        lbvars.add_filter(ctx.guild.id, filter, filter_message, flags)
        e = discord.Embed(title=f"✅ Flags for {filter} filter updated", description=flags)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @cmd_filter.command(name="remove", aliases=["rm", "delete", "del"])
    @commands.check(can_edit_filters)
    async def cmd_filter_remove(self, ctx, *, arg=""):
        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        filter = arg.strip()
        if filter == "":
            await ctx.send(f"{ctx.author.mention} Which word or phrase filter do you want to remove?\n\n(Type `cancel` to cancel the filter removal.)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} Filter removal cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                filter = message.content.strip()
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name
        filter_list = lbvars.get_filter_list(ctx.guild.id)
        if filter not in filter_list:
            await ctx.send(f"{ctx.author.mention} `{filter}` does not exist as a filter. Try adding it with `{ctx.prefix}filter add`.")
            usage.update(ctx)
            return ctx.command.name
        filter_message = filter_list[filter]["message"]
        lbvars.delete_filter(ctx.guild.id, filter)
        e = discord.Embed(title=f"🗑️ Filter for {filter} removed", description=filter_message)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Filter(bot))
