import discord
from discord.ext import commands
from utils import lbvars
from deprecated.sphinx import versionadded

class NoPermissionResponse(commands.CheckFailure):
    pass

@versionadded(version="1.3.2", reason="New discord.ext checks")
def isBotOwner():
    def predicate(ctx):
        developers = [257203526390906880, 210220782012334081, 300763778608267266]
        if (ctx.message.author.id in developers):
            return True
        else:
            raise NoPermissionResponse("You must be a bot developer to use this command")
    return commands.check(predicate)

@versionadded(version="1.3.2", reason="New discord.ext checks")
def isServerAdmin():
    def predicate(ctx):
        try:
            perms = ctx.message.author.permissions_in(ctx.message.channel)
        except AttributeError:
            perms = discord.Permissions(permissions=0)
        if (perms.administrator):
            return True
        else:
            raise NoPermissionResponse("You must be a server administrator to use this command")
    return commands.check(predicate)

@versionadded(version="1.3.2", reason="New discord.ext checks")
def isLmaoAdmin():
    def predicate(ctx):
        if (str(ctx.message.author.id) in lbvars.get_lmao_admin_list(ctx.message.guild.id)):
            return True
        else:
            raise NoPermissionResponse("You must be a lmao admin to use this command")
    return commands.check(predicate)