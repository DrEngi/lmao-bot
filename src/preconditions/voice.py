import discord
from discord.ext import commands

class NotInVoiceChannel(commands.CheckFailure):
    pass

def isInVoiceChannel():
    def predicate(ctx):
        if (not ctx.author.voice or not ctx.author.voice.channel):
            return True
        else:
            raise NotInVoiceChannel("You must be in a voice channel to use this command.")
    return commands.check(predicate)