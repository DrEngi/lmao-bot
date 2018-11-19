import discord
import re
from discord.ext import commands
from utils import lbvars

def get_perms(message):
    try:
        perms = message.author.permissions_in(message.channel)
    except AttributeError:
        perms = discord.Permissions(permissions=0)
    return perms

def is_admin(message):
    return get_perms(message).administrator

def is_lmao_admin(message):
    return is_admin(message) or str(message.author.id) in lbvars.get_lmao_admin_list(message.guild.id) or is_lmao_developer(message)

def is_lmao_developer(message):
    developers = [257203526390906880, 210220782012334081, 300763778608267266]
    return message.author.id in developers

def clean_everyone(ctx, arg):
    if get_perms(ctx.message).mention_everyone:
        return arg
    return re.sub(r"@(everyone|here)", "@\u200b\\1", arg)
