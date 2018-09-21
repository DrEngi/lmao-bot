# For Evan Vinson <3

import discord
from discord.ext import commands
from utils import dbl, usage#, reddit
#import sqlite3
import aiohttp
import asyncio
import socket
import json
import io
import random

#More NSFW commands: https://gist.github.com/PlanetTeamSpeakk/b35ad4dad4dc600730c629a1a037944d

class NSFW:

    slots = ("bot", "reddit_posts")

    def __init__(self, bot):
        self.bot = bot
        self.reddit_posts = {}

    async def init_reddit_posts(self, sub, sort="hot", limit=100):
        headers = {"User-Agent": "Mozilla/5.0"}
        dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
        url = f"https://www.reddit.com/r/{sub}/{sort}.json?limit={limit}"
        async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
            async with aioclient.get(url, headers=headers) as r:
                data = await r.json()
                self.reddit_posts[sub.lower()] = data["data"]["children"]
                dbl_connector.close()
                await aioclient.close()

    @commands.command(name="gonewild")
    async def cmd_gone_wild(self, ctx):
        await ctx.channel.trigger_typing()
        if "gonewild" not in self.reddit_posts:
            await self.init_reddit_posts("gonewild")
        has_voted = await dbl.has_voted(ctx.author.id)
        if ctx.channel.is_nsfw() and has_voted:
            while True:
                post = random.choice(self.reddit_posts["gonewild"])["data"]
                e = discord.Embed(title=post["title"])
                try:
                    if post["post_hint"] == "image":
                        e.set_image(url=post["url"])
                    elif post["post_hint"] == "rich:video":
                        desc = f"_Psst_, I'm a video--[click my link!]({post['url']})"
                        e = discord.Embed(title=post["title"], description=desc)
                        e.set_image(url=post["thumbnail"])
                    else:
                        continue
                    footer = f"Posted by {post['author']} on /r/gonewild"
                    e.set_footer(text=footer)
                    break
                except KeyError:
                    pass
            #await ctx.send(data["data"]["children"][0]["data"]["title"])
            # with io.open("data/test_reddit.json", "w+") as f:
            #     datas = json.dumps(data, indent=4)
            #     f.write(datas)
            await ctx.send(embed=e)
        elif not has_voted:
            desc = "Have you upvoted yet? :smirk:\n\nhttps://discordbots.org/bot/459432854821142529/vote"
            e = discord.Embed(title="HEY", description=desc)
            footer = "(It may take a few minutes to process your vote)"
            e.set_footer(text=footer)
            await ctx.send(embed=e)
        else:
            await ctx.send("Whoa-ho-ho there, pardner, you have to be in an NSFW channel for that! 👀")
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(NSFW(bot))
