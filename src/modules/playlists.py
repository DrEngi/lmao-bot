import math, re, io, json

import discord, lavalink, asyncio
from discord.ext import commands

from utils import lbvars, usage, lbutil
from preconditions import voice

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')

class Playlists:
    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            #This shouldn't be run because we have music going first, but just in case.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('159.89.233.140', 2333, lbvars.lavalinkpass, 'us', 'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

    #@commands.group(name="playlist", aliases=['pl', 'playlists'], invoke_without_command=True)
    @commands.command(name="playlist", aliases=['pl', 'playlists'])
    async def cmd_playlist(self, ctx):
        await ctx.send("Playlists are currently disabled due to ongoing performance issues.")
    
    #     with io.open("../data/playlists.json") as f:
    #         playlist_data = json.load(f)
    #         if str(ctx.guild.id) not in playlist_data:
    #             await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
    #             usage.update(ctx)
    #             return ctx.command.name
    #         guild_pl = playlist_data[str(ctx.guild.id)]

    #         title = f"**Playlists for {ctx.guild.name}**"
    #         desc = f"""
    #             Use `{ctx.prefix}pl info playlist_name` to view `playlist_name`.\n
    #             Use `{ctx.prefix}pl load playlist_name` to load `playlist_name` onto the queue.\n
    #             Use `{ctx.prefix}pl save` to save up to the first 20 songs of the current queue as a playlist.\n
    #             Use `{ctx.prefix}pl remove` to remove a playlist.\n
    #             """
    #         playlists = []
    #         for name, queue in guild_pl.items():
    #             playlists.append((name[:100], len(queue)))

    #         for i in range(math.ceil(len(playlists) / 25)):
    #             e = discord.Embed(title=title, description=desc)
    #             e.set_footer(text=f"Page {i + 1}")
    #             for j in range(25):
    #                 try:
    #                     playlist = playlists[i + j]
    #                     e.add_field(name=playlist[0], value=f"{playlist[1]} song(s)")
    #                 except IndexError:
    #                     break
    #             await ctx.send(embed=e)

    #     usage.update(ctx)
    #     return ctx.command.name

    # @cmd_playlist.command(name="info", alises=['information'])
    # async def cmd_playlist_info(self, ctx, name=""):
    #     with io.open("../data/playlists.json") as f:
    #         playlist_data = json.load(f)
    #         if str(ctx.guild.id) not in playlist_data:
    #             await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
    #             usage.update(ctx)
    #             return ctx.command.name
    #         guild_pl = playlist_data[str(ctx.guild.id)]
        
    #     if name in guild_pl:
    #         playlist = guild_pl[name]
    #         desc = []
    #         full_duration = 0
    #         for i in range(0, math.ceil(len(playlist) / 20)):
    #             desc.append("")
    #         for i in range(0, len(playlist)):
    #             full_duration += playlist[i]["duration"]
    #             line = f"{i + 1}. **{playlist[i]['title']}"
    #             if len(line) > 100:
    #                 line = line[:97] + "..."
    #             line += f"** {lbutil.print_duration(playlist[i]['duration'])}\n"
    #             desc[math.floor(i / 20)] += line
    #         for i in range(0, len(desc)):
    #             e = discord.Embed(title=f"{name} Playlist for {ctx.guild.name} {lbutil.print_duration(full_duration)}", description=desc[i])
    #             e.set_footer(text=f"Page {i + 1}")
    #             await ctx.send(embed=e)
    #     else:
    #         e = discord.Embed(title="Error")
    #     usage.update(ctx)
    #     return ctx.command.name

    # @cmd_playlist.command(name="remove", aliases=["rm", "delete", "del"])
    # async def cmd_playlist_remove(self, ctx, arg=""):
    #     def check(message):
    #         return message.author == ctx.author and message.channel == ctx.channel
    #     name = arg

    #     with io.open("../data/playlists.json") as f:
    #         playlist_data = json.load(f)
    #         if str(ctx.guild.id) not in playlist_data:
    #             await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
    #             usage.update(ctx)
    #             return ctx.command.name
    #         guild_pl = playlist_data[str(ctx.guild.id)]

    #         if name == "":
    #             pl_list = ""
    #             for name, queue in guild_pl.items():
    #                 pl_list += f"`{name}`, "
    #             pl_list = (pl_list[:-2])[:1500]
    #             remove_message = f"{ctx.author.mention} Which playlist should be removed?\n{pl_list}\n(Type `cancel` to cancel the playlist removal.)"

    #             await ctx.send(remove_message)
    #             try:
    #                 message = await self.bot.wait_for("message", timeout=30.0, check=check)
    #                 name = message.content
    #             except asyncio.TimeoutError:
    #                 await ctx.send(f":x: {ctx.author.mention} Command timed out.")
    #                 usage.update(ctx)
    #                 return ctx.command.name

    #         if name not in guild_pl:
    #             await ctx.send(f"`{name}` is not a playlist for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to make it one!")
    #             usage.update(ctx)
    #             return ctx.command.name

    #         await ctx.send(f"{ctx.author.mention} Are you sure you want to delete `{name}`, a playlist with `{len(guild_pl[name])}` song(s)? (Y/N)")
    #         try:
    #             message = await self.bot.wait_for("message", timeout=30.0, check=check)
    #             if "y" not in message.content.lower():
    #                 await ctx.send(f":x: {ctx.author.mention} `{name}` playlist is not removed.")
    #                 usage.update(ctx)
    #                 return ctx.command.name
    #         except asyncio.TimeoutError:
    #             await ctx.send(f":x: {ctx.author.mention} Command timed out.")
    #             usage.update(ctx)
    #             return ctx.command.name

    #         del playlist_data[str(ctx.guild.id)][name]
    #         new_playlist_data = json.dumps(playlist_data, indent=4)
    #         with io.open("../data/playlists.json", "w+") as fo:
    #             fo.write(new_playlist_data)

    #         await ctx.send(f":wastebasket: `{name}` playlist has been removed.")

    #     usage.update(ctx)
    #     return ctx.command.name

    # @cmd_playlist.command(name="save", aliases=["export"])
    # async def cmd_save(self, ctx, *, arg=""):
    #     player = self.bot.lavalink.players.get(ctx.guild.id)
        
    #     if player is None:
    #         e = discord.Embed(title="Command Error", description=f"There is currently no queue to save. Try queuing some songs with `{ctx.prefix} play`.")
    #         await ctx.send(embed=e)
    #         usage.update(ctx)
    #         return ctx.command.name

    #     if not player.queue:
    #         e = discord.Embed(title="Command Error", description=f"There is currently no queue to save. Try queuing some songs with `{ctx.prefix} play`.")
    #         await ctx.send(embed=e)
    #         usage.update(ctx)
    #         return ctx.command.name

    #     def check(message):
    #         return message.author == ctx.author and message.channel == ctx.channel
    #     name = arg

    #     if name == "":
    #         await ctx.send(f"{ctx.author.mention}, What should the playlist name be?\n\n(Note: the playlist name may not contain spaces or line breaks. Type `cancel` to cancel the new playlist.)")
    #         try:
    #             message = await self.bot.wait_for("message", timeout=30.0, check=check)
    #             if message.content.lower() == "cancel":
    #                 await ctx.send(f":x: {ctx.author.mention} New playlist cancelled.")
    #                 usage.update(ctx)
    #                 return ctx.command.name
    #             name = message.content.strip().split()[0].strip()
    #         except asyncio.TimeoutError:
    #             await ctx.send(f":x: {ctx.author.mention} Command timed out.")
    #             usage.update(ctx)
    #             return ctx.command.name

    #     new_playlist = []
    #     length = len(player.queue)
    #     if length > 20:
    #         length = 20
    #     for i in range(length):
    #         new_playlist.append(player.queue[i].to_dict())

    #     with io.open("../data/playlists.json") as f:
    #         playlist_data = json.load(f)
    #         if str(ctx.guild.id) not in playlist_data:
    #             playlist_data[str(ctx.guild.id)] = {}
    #         if name in playlist_data[str(ctx.guild.id)]:
    #             await ctx.send(f"{ctx.author.mention} `{name}` is already a playlist name. Are you sure you want to overwrite this playlist? (Y/N)")
    #             try:
    #                 message = await self.bot.wait_for("message", timeout=30.0, check=check)
    #                 if "y" not in message.content.lower():
    #                     await ctx.send(f":x: {ctx.author.mention} New playlist cancelled.")
    #                     usage.update(ctx)
    #                     return ctx.command.name
    #             except asyncio.TimeoutError:
    #                 await ctx.send(f":x: {ctx.author.mention} Command timed out.")
    #                 usage.update(ctx)
    #                 return ctx.command.name
    #         playlist_data[str(ctx.guild.id)][name] = new_playlist
    #         new_playlist_data = json.dumps(playlist_data, indent=4)
    #         with io.open("../data/playlists.json", "w+") as fo:
    #             fo.write(new_playlist_data)

    #     await ctx.send(f":white_check_mark: `{length}` song(s) in the current queue have been saved as playlist `{name}`.")

    #     usage.update(ctx)
    #     return ctx.command.name

def setup(bot):
    bot.add_cog(Playlists(bot))