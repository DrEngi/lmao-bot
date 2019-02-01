import discord
from discord.ext import commands
import json
import io

# Updates the usage of a given command and its alias
def update(ctx, arg=None):
    name = ctx.command.name
    subcmd = None
    if ctx.command.parent is not None:
        name = ctx.command.parent.name
        subcmd = ctx.command.name
    alias = ctx.invoked_with
    with io.open("data/cmd_usage.json") as f:
        cmd_usage_data = json.load(f)
        if name not in cmd_usage_data:
            cmd_usage_data[name] = {"uses": 0}
        cmd_usage = cmd_usage_data[name]
        cmd_usage["uses"] += 1
        if name != "replaceass" and subcmd is None:
            if alias not in cmd_usage:
                cmd_usage[alias] = 0
            cmd_usage[alias] += 1
            if arg is not None and f"{name}:{arg}" not in cmd_usage:
                cmd_usage[f"{name}:{arg}"] = 0
            if arg is not None:
                cmd_usage[f"{name}:{arg}"] += 1
        elif subcmd is not None:
            if subcmd not in cmd_usage:
                cmd_usage[subcmd] = {"uses": 0}
            if alias not in cmd_usage[subcmd]:
                cmd_usage[subcmd][alias] = 0
            cmd_usage[subcmd]["uses"] += 1
            cmd_usage[subcmd][alias] += 1
        new_cmd_data = json.dumps(cmd_usage_data, indent=4)
        with io.open("data/cmd_usage.json", "w+", encoding="utf-8") as fo:
            fo.write(new_cmd_data)

def count_total_members(bot):
    total = 0
    for guild in bot.guilds:
        total += guild.member_count
    return total
