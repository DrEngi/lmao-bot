import discord
from discord.ext import commands
from utils import lbvars, usage, perms
import asyncio
import math
from datetime import datetime

class Mod(commands.Cog):

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="adminlist", aliases=["listadmins"])
    async def cmd_admin_list(self, ctx):
        title = f"**lmao administrators for {ctx.guild.name}**"
        admins = []
        for admin in lbvars.get_lmao_admin_list(ctx.guild.id):
            admins.append(ctx.guild.get_member(int(admin)).name)
        for i in range(int(math.ceil(len(admins) / 25))):
            desc = ""
            for j in range(25):
                try:
                    desc += admins[i + j] + "\n"
                except IndexError:
                    break
            e = discord.Embed(title=title, description=desc)
            e.set_footer(text=f"Page {i + 1}")
            await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="addadmin")
    async def cmd_add_admin(self, ctx, *, arg=""):
        if perms.is_lmao_admin(ctx.message):
            if len(ctx.message.mentions) == 1:
                if str(ctx.message.mentions[0].id) in lbvars.get_lmao_admin_list(ctx.guild.id):
                    await ctx.send(ctx.message.mentions[0].name + " is already a lmao administrator.")
                else:
                    lbvars.add_lmao_admin(ctx.guild.id, ctx.message.mentions[0].id)
                    await ctx.send(ctx.message.mentions[0].mention + " has been added as a lmao administrator for this guild.")
            elif len(ctx.message.mentions) > 1:
                await ctx.send(f"{ctx.author.mention} You may only add one lmao administrator at a time.")
            elif len(ctx.message.mentions) < 1:
                await ctx.send(f"{ctx.author.mention} You must mention the user you want to add as a lmao administrator.")
        else:
            await ctx.send(f"{ctx.author.mention} Only guild administrators and lmao administrators can add other lmao administrators.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="removeadmin", aliases=["deleteadmin"])
    async def cmd_remove_admin(self, ctx, *, arg=""):
        if perms.is_admin(ctx.message) or perms.is_lmao_developer(ctx.message):
            if len(ctx.message.mentions) == 1:
                if str(ctx.message.mentions[0].id) not in lbvars.get_lmao_admin_list(ctx.guild.id):
                    await ctx.send(ctx.message.mentions[0].name + " is not a lmao administrator.")
                else:
                    lbvars.set_lmao_admin_list(ctx.guild.id, [admin for admin in lbvars.get_lmao_admin_list(ctx.guild.id) if admin != str(ctx.message.mentions[0].id)])
                    await ctx.send(ctx.message.mentions[0].mention + " has been removed as a lmao administrator for this guild.")
            elif len(ctx.message.mentions) > 1:
                await ctx.send(f"{ctx.author.mention} You may only remove one lmao administrator at a time.")
            elif len(ctx.message.mentions) < 1:
                await ctx.send(f"{ctx.author.mention} You must mention the user you want to remove as a lmao administrator.")
        else:
            await ctx.send(f"{ctx.author.mention} Only guild administrators can remove lmao administrators.")
        usage.update(ctx)
        return ctx.command.name

    # @commands.command(name="disable")
    # async def cmd_disable(self, ctx, *, arg=""):
    #     cmd = arg.strip()
    #     if cmd == "":
    #         #TODO: Instead of error message, prompt the user
    #         await ctx.send(f"To disable a command, use `{ctx.prefix}disable command_name`, where `command_name` is the name of the command you want to disable. e.g. `{ctx.prefix}disable someone`\n\n" \
    #             "Not that not all commands can be disabled and that only lmao administrators and server administrators can enable/disable commands.")
    #         usage.update(ctx)
    #         return ctx.command.name
    #     #disable here
    #     usage.update(ctx)
    #     return ctx.command.name

    @commands.command(name="purge", aliases=["clear", "clean", "prune"])
    async def cmd_purge(self, ctx, *, arg=""):  # Allows the deletion of messages
        if perms.get_perms(ctx.message).manage_messages or perms.is_lmao_admin(ctx.message):
            try:
                if int(arg) > 100:
                    await ctx.send("You cannot delete more than 100 messages.")
                elif int(arg) > 0:
                    deleted = await ctx.channel.purge(limit=int(arg) + 1)
                    try:
                        await ctx.send(f"**Successfully deleted {len(deleted) - 1} message(s).**", delete_after=3)
                    except:
                        lbvars.LOGGER.info("Exception when purging message")
                elif int(arg) == 0:
                    await ctx.send(f"{ctx.author.mention} I'm always deleting 0 messages. You don't need to call a command for that.")
                else:
                    await ctx.send(f"{ctx.author.mention} What, you think I'm some sort of magician who can delete a negative number of messages?")
            except ValueError:
                await ctx.send(f"{ctx.author.mention} You must specify the number of messages to purge. e.g. `{ctx.prefix}purge 5`")
            except discord.errors.Forbidden:
                await ctx.send(f"{ctx.author.mention} The messages could not be purged due to insufficient permissions for lmao-bot. Make sure `Manage Messages` is enabled for lmao-bot.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to manage messages.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="mute")
    async def cmd_mute(self, ctx, *, arg=""):
        #muted_perms = discord.Permissions(send_messages=False)
        #lmao_muted = await ctx.guild.create_role(name="lmao muted", permissions=muted_perms)
        if perms.get_perms(ctx.message).manage_channels or perms.is_lmao_admin(ctx.message):
            try:
                if len(ctx.message.mentions) == 1:
                    if ctx.message.mentions[0] == self.bot.user:
                        await ctx.send(f"Silly {ctx.author.mention}, I can't mute myself!")
                    elif ctx.message.mentions[0].id == 210220782012334081:
                        await ctx.send(f"Please, {ctx.author.mention}, you can't mute my creator.")
                    else:
                        mute_time = 0
                        if arg.find(" ") != -1:
                            try:
                                mute_time = int(arg[:arg.find(" ")])
                                if mute_time <= 0:
                                    mute_time = 0
                            except ValueError:
                                mute_time = 0
                        muted_perms = ctx.channel.overwrites_for(ctx.message.mentions[0])
                        muted_perms.send_messages = False
                        await ctx.channel.set_permissions(ctx.message.mentions[0], overwrite=muted_perms)
                        #await ctx.message.mentions[0].add_roles(lmao_muted)
                        after_msg = ""
                        if mute_time != 0:
                            after_msg += f" for {mute_time} minutes"
                        after_msg += "."
                        await ctx.send(f"{ctx.message.mentions[0].mention} was muted in {ctx.channel.mention} by {ctx.author.mention}{after_msg}")
                        if mute_time != 0:
                            await asyncio.sleep(mute_time * 60)
                            muted_perms = ctx.channel.overwrites_for(ctx.message.mentions[0])
                            muted_perms.send_messages = None
                            await ctx.channel.set_permissions(ctx.message.mentions[0], overwrite=muted_perms)
                elif len(ctx.message.mentions) < 1:
                    await ctx.send(f"{ctx.author.mention} You must mention the user you want to mute on this channel.")
                elif len(ctx.message.mentions) > 1:
                    await ctx.send(f"{ctx.author.mention} You may not mute more than one member at a time.")
            except discord.errors.Forbidden:
                await ctx.send(f"{ctx.author.mention} lmao-bot eithers lacks the permission to mute members or the member you tried to mute is of an equal or higher role than lmao-bot. Make sure `Manage Channels` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to mute.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to mute members.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="unmute")
    async def cmd_unmute(self, ctx, *, arg=""):
        if perms.get_perms(ctx.message).manage_channels or perms.is_lmao_admin(ctx.message):
            try:
                if len(ctx.message.mentions) == 1:
                    unmuted_perms = ctx.channel.overwrites_for(ctx.message.mentions[0])
                    unmuted_perms.send_messages = None
                    await ctx.channel.set_permissions(ctx.message.mentions[0], overwrite=unmuted_perms)
                    await ctx.send(f"{ctx.message.mentions[0].mention} was unmuted in {ctx.channel.mention} by {ctx.author.mention}.")
                elif len(ctx.message.mentions) < 1:
                    await ctx.send(f"{ctx.author.mention} You must mention the user you want to unmute on this channel.")
                elif len(ctx.message.mentions) > 1:
                    await ctx.send(f"{ctx.author.mention} You may not unmute more than one member at a time.")
            except discord.errors.Forbidden:
                await ctx.send(f"{ctx.author.mention} lmao-bot eithers lacks the permission to unmute members or the member you tried to unmute is of an equal or higher role than lmao-bot. Make sure `Manage Channels` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to unmute.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to unmute members.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="kick", aliases=["getouttahere"])
    async def cmd_kick(self, ctx, *, arg=""):
        if not perms.get_perms(ctx.message).kick_members and not perms.is_lmao_admin(ctx.message):
            await ctx.send(f"{ctx.author.mention} You do not have the permission to kick members.")
            usage.update(ctx)
            return ctx.command.name
        try:
            if len(ctx.message.mentions) == 1:
                to_kick = ctx.message.mentions[0]
                if to_kick == self.bot.user:
                    await ctx.send(f"Silly {ctx.author.mention}, I can't kick myself!")
                elif to_kick.id == 210220782012334081:
                    await ctx.send(f"Please, {ctx.author.mention}, you can't kick my creator.")
                else:
                    reason = arg.replace(to_kick.mention, "").strip()
                    reason_message = f"Reason: {reason}"
                    if reason == "":
                        reason_message = "No reason given."
                    e = discord.Embed(title=f"You have been kicked from {ctx.guild.name} by {ctx.author}", description=reason_message, timestamp=datetime.now())
                    await to_kick.send(embed=e)
                    await to_kick.kick(reason=reason)
                    await ctx.send(f"Goodbye, {to_kick}, I'll see you in therapy!")
            elif len(ctx.message.mentions) < 1:
                await ctx.send(f"{ctx.author.mention} You must mention the user you want to kick from the guild.")
            elif len(ctx.message.mentions) > 1:
                await ctx.send(f"{ctx.author.mention} You may not kick more than one member at a time.")
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention} lmao-bot eithers lacks the permission to kick members or the member you tried to kick is of an equal or higher role than lmao-bot. Make sure `Kick Members` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to kick.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="ban")
    async def cmd_ban(self, ctx, *, arg=""):
        if not perms.get_perms(ctx.message).ban_members and not perms.is_lmao_admin(ctx.message):
            await ctx.send(f"{ctx.author.mention} You do not have the permission to ban members.")
            usage.update(ctx)
            return ctx.command.name
        try:
            if len(ctx.message.mentions) == 1:
                to_ban = ctx.message.mentions[0]
                if to_ban == self.bot.user:
                    await ctx.send(f"Silly {ctx.author.mention}, I can't ban myself!")
                elif to_ban.id == 210220782012334081:
                    await ctx.send(f"Please, {ctx.author.mention}, you can't ban my creator.")
                elif to_ban.id == ctx.author.id:
                    await ctx.send(f"{ctx.author.mention}, you can't ban yourself.")
                else:
                    reason = arg.replace(to_ban.mention, "").strip()
                    reason_message = f"Reason: {reason}"
                    if reason == "":
                        reason_message = "No reason given."
                    e = discord.Embed(title=f"You have been banned from {ctx.guild.name} by {ctx.author}", description=reason_message, timestamp=datetime.now())
                    await to_ban.send(embed=e)
                    await to_ban.ban(reason=reason)
                    await ctx.send(f"Goodbye, {to_ban}, I'll see you in therapy! (Or never, 'cause, you know, you're banned...)")
            elif len(ctx.message.mentions) < 1:
                await ctx.send(f"{ctx.author.mention} You must mention the user you want to ban from the guild.")
            elif len(ctx.message.mentions) > 1:
                await ctx.send(f"{ctx.author.mention} You may not ban more than one member at a time.")
        except discord.errors.Forbidden:
            await ctx.send(f"{ctx.author.mention} lmao-bot eithers lacks the permission to ban members or the member you tried to ban is of an equal or higher role than lmao-bot. Make sure `Ban Members` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to ban.")
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Mod(bot))
