import discord
from discord.ext import commands

class NotInVoiceChannel(commands.CheckFailure):
    pass

class InvalidVoicePermissions(commands.CheckFailure):
    pass

def isInVoiceChannel():
    def predicate(ctx):
        if ctx.author.voice is not None and ctx.author.voice.channel is not None:
            return True
        else:
            raise NotInVoiceChannel("You must be in a voice channel to use this command.")
    return commands.check(predicate)

def hasValidVoicePermissions():
    def predicate(ctx):
        permissions = ctx.author.voice.channel.permissions_for(ctx.me)

        if not permissions.connect or not permissions.speak:  # Check user limit too?
            raise InvalidVoicePermissions("Missing permissions")
        else:
            return True
    return commands.check(predicate)