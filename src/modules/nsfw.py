# For Evan Vinson <3

import discord
from discord.ext import commands
from utils import lbvars, perms, dbl, usage#, reddit
import urllib.request
import requests
#import sqlite3
import aiohttp
import asyncio
import socket
import json
import io
import random
import os
import html
import rule34

#More NSFW commands: https://gist.github.com/PlanetTeamSpeakk/b35ad4dad4dc600730c629a1a037944d

def url_exists(url):
    """Checks if a URL is valid"""
    if url == "":
        return False
    request = requests.get(url)
    if request.status_code == 200:
        return True
    else:
        return False

class Category:

    def __init__(self, name, icon):
        self.name = name
        self.icon = icon

class NSFW(commands.Cog):

    slots = ("bot", "reddit_posts", "categories")

    def __init__(self, bot):
        self.bot = bot
        self.reddit_posts = {}
        self.categories = {
            "ass": Category("ass", "🍑"),
            "boobs": Category("boobs", "🍈"),
            "pussy": Category("pussy", "🌮"),
            "dick": Category("dick", "🍆"),
            "hentai": Category("hentai", "🐙")
        }

    async def __local_check(self, ctx):
        """Checks if the guild allows NSFW commands; if not, then don't run commands"""
        allow_nsfw = ctx.command.name == "nsfwtoggle" or lbvars.get_allow_nsfw(ctx.guild.id)
        if not allow_nsfw:
            await ctx.send(f"{ctx.author.mention} NSFW commands are not allowed on this Christian Discord server. :angel:")
        return allow_nsfw

    async def check_voted(self, ctx):
        has_voted = await dbl.has_voted(ctx.author.id)
        if ctx.channel.is_nsfw() and has_voted:
            return True
        elif not has_voted:
            desc = "Have you upvoted yet? :smirk:\n\nhttps://discordbots.org/bot/459432854821142529/vote"
            e = discord.Embed(title="HEY", description=desc)
            footer = "(It may take a few minutes to process your vote)"
            e.set_footer(text=footer)
            await ctx.send(embed=e)
            return False
        else:
            await ctx.send("Whoa-ho-ho there, pardner, you have to be in an NSFW channel for that! 👀")
            return False

    async def init_reddit_posts(self, sub, sort="hot", limit=100):
        headers = {"User-Agent": "Mozilla/5.0"}
        dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
        url = f"https://www.reddit.com/r/{sub}/{sort}.json?limit={limit}"
        async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
            async with aioclient.get(url, headers=headers) as r:
                data = await r.json()
                self.reddit_posts[sub.lower()] = data["data"]["children"]
                await dbl_connector.close()
                await aioclient.close()

    async def send_rand_img(self, ctx, category):
        with io.open("../data/nsfw_urls.json") as f:
            urls = json.load(f)
        url = ""
        while not url_exists(url):
            url = random.choice(urls[category])
        cat = self.categories[category]
        e = discord.Embed(title=cat.icon)
        e.set_image(url=url)
        await ctx.send(embed=e)

    @commands.command(name="nsfwtoggle", aliases=["togglensfw", "nsfwon", "nsfwoff"])
    async def cmd_toggle_nsfw(self, ctx):
        if not perms.get_perms(ctx.message).manage_messages and not perms.is_lmao_admin(ctx.message):
            await ctx.send(f"{ctx.author.mention} You do not have the permission to toggle NSFW settings for your guild.")
            usage.update(ctx)
            return ctx.command.name
        if ctx.invoked_with == "nsfwon":
            allow_nsfw = lbvars.set_allow_nsfw(ctx.guild.id, True)
        elif ctx.invoked_with == "nsfwoff":
            allow_nsfw = lbvars.set_allow_nsfw(ctx.guild.id, False)
        else:
            allow_nsfw = lbvars.toggle_allow_nsfw(ctx.guild.id)
        if (allow_nsfw):
            await ctx.send(f":smirk: What's wrong, big boy? Never had your server filled with porn by a bot before?\n\n(NSFW commands enabled for {ctx.guild.name})")
        else:
            await ctx.send(":angel: No NSFW content is allowed on this Christian Discord server.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="gonewild", aliases=["ladybonersgw", "gonewildmale", "thighhighs"])
    async def cmd_gone_wild(self, ctx):
        sub = ctx.invoked_with
        if sub == "gonewildmale":
            sub = "ladybonersgw"
        await ctx.channel.trigger_typing()
        if sub not in self.reddit_posts:
            await self.init_reddit_posts(sub)
        if await self.check_voted(ctx):
            while True:
                post = random.choice(self.reddit_posts[sub])["data"]
                title = html.unescape(post["title"])
                permalink = f"https://www.reddit.com{post['permalink']}"
                e = discord.Embed(title=title, url=permalink)
                try:
                    if post["post_hint"] == "image":
                        e.set_image(url=post["url"])
                    elif post["post_hint"] == "rich:video":
                        desc = f"_Psst_, I'm a video--[click my link!]({post['url']})"
                        e = discord.Embed(title=title, description=desc)
                        e.set_image(url=post["thumbnail"])
                    else:
                        continue
                    footer = f"Posted by {html.unescape(post['author'])} on /r/{sub}"
                    e.set_footer(text=footer)
                    break
                except KeyError:
                    pass
            await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="nsfw", aliases=["pussy", "dick", "ass", "boobs", "hentai"])
    async def cmd_nsfw(self, ctx):
        await ctx.channel.trigger_typing()
        if await self.check_voted(ctx):
            if ctx.invoked_with == "nsfw":
                nsfw_commands = """😳 `{0}nsfwtoggle` Toggles whether NSFW commands are allowed on the server or not.
                   \n🍑 `{0}ass` Sends a random NSFW ass picture.
                   \n🍈 `{0}boobs` Sends a random NSFW boobs picture.
                   \n🌮 `{0}pussy` Sends a random NSFW pussy picture.
                   \n🍆 `{0}dick` Sends a random NSFW dick picture.
                   \n🐙 `{0}hentai` Sends a random NSFW hentai GIF.
                   \n👩 `{0}gonewild` Sends a random post from the NSFW /r/gonewild subreddit.
                   \n👨 `{0}gonewildmale` Sends a random post from the NSFW /r/Ladybonersgw subreddit.
                   \n🧦 `{0}thighhighs` Sends a random post from the NSFW /r/thighhighs subreddit.
                   \n🖌️ `{0}rule34` `search_term` Sends a random NSFW Rule 34 post for `search_term`.
                   \n🖌️ `{0}r34` `search_term` Does the same thing as `{0}rule34`."""
                e = discord.Embed(title="😏 **NSFW Commands** 😏", description=nsfw_commands.format(ctx.prefix), color=0xD11919)
                await ctx.send(embed=e)
                usage.update(ctx)
                return ctx.command.name
            await self.send_rand_img(ctx, ctx.invoked_with.lower())
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="rule34", aliases=["r34"])
    async def cmd_rule_34(self, ctx, *, arg=""):
        await ctx.channel.trigger_typing()
        if await self.check_voted(ctx):
            search = arg.replace(" ", "_")
            r34 = rule34.Rule34(self.bot.loop)
            urls = await r34.getImageURLS(search)
            if urls is None:
                urls = await r34.getImageURLS(arg)
            if urls is not None:
                e = discord.Embed(title=f"Rule 34 {arg}")
                e.set_image(url=random.choice(urls))
                await ctx.send(embed=e)
            else:
                await ctx.send(f"{ctx.author.mention} No Rule 34 results found for {arg}. :pensive:")
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(NSFW(bot))
