### TODO: ###
# Force a 15-second vote (50%) for voice channels with at least 3 non-bot users when someone tries to skip
    # skip_vote variable in class?
    # stop_vote ?
# Perhaps consider permissions
# Add multiple options for videos to play upon searching
# Consider using this for to_dict: https://stackoverflow.com/questions/61517/python-dictionary-from-an-objects-fields

"""
Please understand Music bots are complex, and that even this basic example can be daunting to a beginner.
For this reason it's highly advised you familiarize yourself with discord.py, python and asyncio, BEFORE
you attempt to write a music bot.
This example makes use of: Python 3.6
For a more basic voice example please read:
    https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
This is a very basic playlist example, which allows per guild playback of unique queues.
The commands implement very basic logic for basic usage. But allow for expansion. It would be advisable to implement
your own permissions and usage logic for commands.
e.g You might like to implement a vote before skipping the song or only allow admins to stop the player.
Music bots require lots of work, and tuning. Goodluck.
If you find any bugs feel free to ping me on discord. @Eviee#0666
"""
import discord
from discord.ext import commands
from utils import usage, lbutil

import asyncio
import itertools
import sys
import traceback
import io
import json
import time
import os
import math
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL
from utils import perms

client = discord.Client()

def current_time():
    return time.time()

def get_ytdlopts(guild_id):
    ytdlopts = {
        "format": "bestaudio/best",
        "outtmpl": f"downloads/%(extractor)s-%(id)s-{guild_id}.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": True,#False,
        "quiet": False,#True,
        "no_warnings": False,#True,
        "default_search": "auto",
        "source_address": "0.0.0.0"  # ipv6 addresses cause issues sometimes
    }
    return ytdlopts

ffmpegopts = {
    "before_options": "-nostdin",
    "options": "-vn"
}

ytdl = {}
#YoutubeDL(ytdlopts)

class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""

class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

def print_duration(time, brackets=True):
    t = lbutil.dhms_time(time)
    h = t["h"] + 24 * t["d"]
    m = str(t["m"])
    s = str(t["s"])
    if len(s) < 2:
        s = "0" + s
    m = str(m)
    if len(m) < 2:
        m = "0" + m
    if h > 0:
        out = f"{h}:{m}:{s}"
    else:
        out = f"{m}:{s}"
    if brackets:
        out = f"[{out}]"
    return out
def print_date(yyyymmdd):
    return f"{yyyymmdd[:4]}-{yyyymmdd[4:6]}-{yyyymmdd[6:]}"

class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get("title")
        self.web_url = data.get("webpage_url")
        self.url = data.get("url")
        self.duration = data.get("duration")
        self.uploader = data.get("uploader")
        self.upload_date = data.get("upload_date")
        self.id = data.get("id")
        self.extractor = data.get("extractor")
        self.ext = data.get("ext")

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    def __str__(self):
        return f"**{self.title}** {print_duration(self.duration)}"

    def get_path(self, guild_id):
        return f"downloads/{self.extractor}-{self.id}-{guild_id}.{self.ext}"

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = asyncio.get_event_loop()
        if ctx.guild.id not in ytdl:
            ytdl[ctx.guild.id] = YoutubeDL(get_ytdlopts(ctx.guild.id))

        to_run = partial(ytdl[ctx.guild.id].extract_info, url=search, download=download)
        try:
            data = await loop.run_in_executor(None, to_run)
        except Exception as e:
            e_name = type(e).__name__
            if e_name == "DownloadError":
                await ctx.send(f":x: {ctx.author.mention} No results were found on YouTube for {search}. Try searching for the video's URL.")
            else:
                await ctx.send(f"{ctx.author.mention} Error: {e_name}. If you are receiving this message, please file a bug report to the support server (`{ctx.prefix}support` provides a link).")
            return None

        if "entries" in data:
            # BRILLIANCY: Show up to 5 options, let user choose
            # take first item from a playlist
            data = data["entries"][0]

        e = discord.Embed(title=f"✅ Added **{data['title']}** to the queue.")
        e.add_field(name="Duration", value=print_duration(data["duration"]))
        e.add_field(name="Uploader", value=data["uploader"])
        e.add_field(name="Upload Date", value=print_date(data["upload_date"]))
        e.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=e)

        if download:
            source = ytdl[ctx.guild.id].prepare_filename(data)
        else:
            source_dict = {
                "webpage_url": data["webpage_url"],
                "requester": ctx.author,
                "title": data["title"],
                "duration": data["duration"],
                "url": data["url"],
                "uploader": data["uploader"],
                "upload_date": data["upload_date"],
                "id": data["id"],
                "extractor": data["extractor"],
                "ext": data["ext"]
            }
            source_info = YTInfo(source_dict)
            return source_info
        source = ytdl[ctx.guild.id].prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    # @classmethod
    # async def duplicate_source(cls, ctx):
    #     #CONTINUE

    @classmethod
    async def regather_stream(cls, ctx, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data.requester

        to_run = partial(ytdl[ctx.guild.id].extract_info, url=data.webpage_url, download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)

class YTInfo:
    def __init__(self, info: dict):
        self.webpage_url = info["webpage_url"]
        self.requester = info["requester"]
        self.title = info["title"]
        self.duration = info["duration"]
        self.url = info["url"]
        self.uploader = info["uploader"]
        self.upload_date = info["upload_date"]
        self.id = info["id"]
        self.extractor = info["extractor"]
        self.ext = info["ext"]

    def __str__(self):
        return f"**{self.title}** {print_duration(self.duration)}"

    def get_path(self, guild_id):
        return f"downloads/{self.extractor}-{self.id}-{guild_id}.{self.ext}"

    def to_dict(self):
        YTInfoDict = {
            "webpage_url": self.webpage_url,
            "requester": None,
            "title": self.title,
            "duration": self.duration,
            "url": self.url,
            "uploader": self.uploader,
            "upload_date": self.upload_date,
            "id": self.id,
            "extractor": self.extractor,
            "ext": self.ext
        }
        return YTInfoDict

class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice its instance will be destroyed.
    """

    __slots__ = ("ctx", "bot", "_guild", "_channel", "_cog", "queue", "volume", "loop_queue", "np")

    def __init__(self, ctx):
        self.ctx = ctx
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog
        self.volume = .5
        self.loop_queue = False

        self.queue = []
        self.np = None

    async def set_np(self):
        self.np = await YTDLSource.regather_stream(self.ctx, self.queue[0], loop=self.bot.loop)

    def next_song(self, error):
        if error:
            print(f"Error: {error} trying to play next song. Guild: {self._guild.name} ({self._guild.id}).")
        # path = self.np.get_path(self._guild.id)
        if self.loop_queue:
            self.queue.append(self.queue[0])
        self.queue.pop(0)
        if len(self.queue) > 0:
            coro = self.set_np()
            fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Error in coro: {e} trying to regather stream. Guild: {self._guild.name} ({self._guild.id}).")
            self.ctx.voice_client.play(self.np, after=self.next_song)
            coro = self.send_np()
        else:
            self.destroy(self._guild)
            coro = self.send_np(finished=True)
        fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Error in coro: {e} trying to send now playing message. Guild: {self._guild.name} ({self._guild.id}).")
        # print(path + " to be removed...")
        # os.remove(path)
        # print(path + " REMOVED")

    async def send_np(self, finished=False):
        if len(self.queue) > 0:
            source = self.np#self.queue[0]
            e = discord.Embed(title=f"▶️ Now playing **{source.title}**.")
            e.add_field(name="Duration", value=print_duration(source.duration))
            e.add_field(name="Uploader", value=source.uploader)
            e.add_field(name="Upload Date", value=print_date(source.upload_date))
            if source.requester is not None:
                e.set_footer(text=f"Requested by {source.requester}")
            await self._channel.send(embed=e)
        elif finished:
            await self._channel.send("⏹️ The queue has finished.")
        else:
            await self._channel.send(f"I am currently not playing anything, but you can add songs for me to play with `{self.ctx.prefix}play`!")

    def print_total_time(self, brackets=True):
        total_duration = 0
        for song in self.queue:
            total_duration += song.duration
        return print_duration(total_duration, brackets)

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music:
    """Music related commands."""

    __slots__ = ("bot", "players")

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        # pops = len(self.players[guild.id].queue) - 1
        # for i in range(0, pops):
            # path = self.players[guild.id].queue[1].get_path(guild.id)
            # self.players[guild.id].queue.pop(1)
            # print(f"Cleanup, removing {path}...")
            # os.remove(path)
            # print("All cleaned")

        try:
            del self.players[guild.id].queue[1:]
        except KeyError:
            pass

        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send("This command can not be used in Private Messages.")
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send("Error connecting to Voice Channel. "
                           "Please make sure you are in a valid channel or provide me with one")

        print("Ignoring exception in command {}:".format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player
        return player

    async def is_in_channel(self, ctx):
        try:
            channel = ctx.author.voice.channel
            return True
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} You must join a voice channel to use music and voice commands.")
            return False

    @classmethod
    async def is_in_channel(cls, ctx):
        try:
            channel = ctx.author.voice.channel
            return True
        except AttributeError:
            await ctx.send(f"{ctx.author.mention} You must join a voice channel to use music and voice commands.")
            return False

    @commands.command(name="allmusic", hidden=True)
    async def cmd_all_music(self, ctx):
        if perms.is_lmao_developer(ctx.message):
            with io.open("management/all_music.txt", "w") as f:
                out = ""
                for guild, player in self.players.items():
                    out += f"{guild} {self.bot.get_guild(int(guild))}\n"
                    for song in player.queue:
                        out += f"{song}\n"
                    out += "\n"
                f.write(out)
                if out.strip() != "":
                    await ctx.send(out[:2000])
                else:
                    await ctx.send("No one is playing music at the moment.")

    @commands.command(name="connect", aliases=["join"])
    async def cmd_connect(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError: #TODO: Perhaps make this quiet?
                raise InvalidVoiceChannel(f"{ctx.author.mention} Please join or specify a voice channel to play music.")

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f"Moving to channel: <{channel}> timed out.")
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f"Connecting to channel: <{channel}> timed out.")

        await ctx.send(embed=discord.Embed(title="🎤 Connected to Voice Channel", description=f"`{channel}`"))

    @commands.command(name="play", aliases=["sing"])
    async def cmd_play(self, ctx, *, arg=""):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        search = arg
        if search.strip() == "":
            await ctx.invoke(self.cmd_resume)
            usage.update(ctx)
            return ctx.command.name

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.cmd_connect)

        player = self.get_player(ctx)

        try:
            i = int(search) - 1
            if i > 0 and i < len(player.queue):
                player.queue.insert(1, player.queue[0])
                player.queue.insert(1, player.queue[i + 1])
                player.queue.pop(i + 2)
                ctx.voice_client.stop()
                usage.update(ctx)
                return ctx.command.name
        except ValueError:
            pass

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)
        if source is None:
            usage.update(ctx)
            return ctx.command.name

        player.queue.append(source)
        if len(player.queue) == 1:
            ##### HOLD ON A GOSH-DARN-DIDDLY SECOND, will this produce more terminating streams if the queue is too long?
            player.np = await YTDLSource.regather_stream(ctx, player.queue[0], loop=self.bot.loop)
            ctx.guild.voice_client.play(player.np, after=player.next_song)
            e = discord.Embed(title=f"▶️ Now playing **{source.title}**.")
            e.add_field(name="Duration", value=print_duration(source.duration))
            e.add_field(name="Uploader", value=source.uploader)
            e.add_field(name="Upload Date", value=print_date(source.upload_date))
            if source.requester is not None:
                e.set_footer(text=f"Requested by {source.requester}")
            await ctx.channel.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="pause")
    async def cmd_pause(self, ctx):
        """Pause the currently playing song."""
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(f"{ctx.author.mention} There are no songs currently in the queue. Why not add some with `{ctx.prefix}play`? :thinking:")
        elif vc.is_paused():
            return

        vc.pause()

        player = self.get_player(ctx)
        await ctx.send(f":pause_button: {ctx.author} paused {player.np}.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="resume", aliases=["unpause"])
    async def cmd_resume(self, ctx):
        """Resume the currently paused song."""
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"{ctx.author.mention} There are no songs currently in the queue. Maybe you should add some with `{ctx.prefix}play`... :thinking:")
        elif not vc.is_paused():
            return

        vc.resume()

        player = self.get_player(ctx)
        await ctx.send(f":play_pause: {ctx.author} resumed {player.np}.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="skip", aliases=["next"])
    async def cmd_skip(self, ctx):
        """Skip the song."""
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        player = self.get_player(ctx)

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"{ctx.author.mention} There are no songs currently in the queue. Try using `{ctx.prefix}play` to jam out to some tunes.")

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        await ctx.send(f":next_track: {ctx.author} skipped {player.np}.")
        vc.stop()
        usage.update(ctx)
        return ctx.command.name

    @commands.group(invoke_without_command=True, name="queue", aliases=["q"])
    async def cmd_queue(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to a voice channel.")

        player = self.get_player(ctx)
        if len(player.queue) < 1:
            return await ctx.send(f"There are currently no queued songs. Use `{ctx.prefix}play` to start playing music!")

        desc = []
        for i in range(0, math.ceil(len(player.queue) / 20)):
            desc.append("")
        for i in range(0, len(player.queue)):
            line = f"{i + 1}. {player.queue[i]}"
            if len(line) > 100:
                line = line[:97] + "..."
            line += "\n"
            desc[math.floor(i / 20)] += line
        for i in range(0, len(desc)):
            e = discord.Embed(title=f"Current Queue for {ctx.guild.name} {player.print_total_time()}", description=desc[i])
            e.set_footer(text=f"Page {i + 1}")
            await ctx.send(embed=e)

        usage.update(ctx)
        return ctx.command.name

    @cmd_queue.command(name="add", aliases=["play"])
    async def cmd_queue_add(self, ctx, *, arg=""):
        await ctx.invoke(self.cmd_play, arg=arg)
        usage.update(ctx)
        return ctx.command.name

    @cmd_queue.command(name="remove", aliases=["delete"])
    async def cmd_queue_remove(self, ctx, *, arg=""):
        in_channel = await Music.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        try:
            to_remove = int(arg)
        except ValueError:
            await ctx.send(f"{ctx.author.mention} To remove a song from the queue, you have to include the number of the song on the playlist you want to remove.\n\ne.g.`{ctx.prefix}q remove 3`")
            usage.update(ctx)
            return ctx.command.name

        player = self.get_player(ctx)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(f"{ctx.author.mention} There are no songs to remove. :pensive:")
            usage.update(ctx)
            return ctx.command.name

        if to_remove < 1 or to_remove > len(player.queue):
            await ctx.send(f"{ctx.author.mention} The number you sent is not a valid song in the queue. Try removing a number from 1 to {len(player.queue)}.")
            usage.update(ctx)
            return ctx.command.name
        await ctx.send(f":heavy_minus_sign: {ctx.author} removed {player.queue[to_remove - 1]} from the queue.")
        if to_remove == 1:
            await ctx.invoke(self.cmd_skip)
            usage.update(ctx)
            return ctx.command.name
        else:
            player.queue.pop(to_remove - 1)
        usage.update(ctx)
        return ctx.command.name

    @cmd_queue.command(name="clear", aliases=["wipe"])
    async def cmd_queue_clear(self, ctx):
        in_channel = await Music.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        player = self.get_player(ctx)
        vc = ctx.voice_client
        if not vc or not vc.is_connected():
            await ctx.send(f"{ctx.author.mention} There is no queue to clear. :pensive:")
            usage.update(ctx)
            return ctx.command.name

        clear_count = len(player.queue) - 1
        del player.queue[1:]
        await ctx.send(f":wastebasket: {ctx.author} cleared {clear_count} songs from the queue.")

        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="nowplaying", aliases=["np", "current", "currentsong", "playing"])
    async def cmd_now_playing(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send(f"{ctx.author.mention} I am not currently in a voice channel. Try `{ctx.prefix}play`, maybe.")
            usage.update(ctx)
            return ctx.command.name

        player = self.get_player(ctx)
        if len(player.queue) == 0:
            await ctx.send(f"{ctx.author.mention} I'm not currently playing anything, but I could be :thinking: (psst, use `{ctx.prefix}play`).")
            usage.update(ctx)
            return ctx.command.name

        await player.send_np()

        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="volume", aliases=["vol"])
    async def cmd_volume(self, ctx, *, arg=""):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 0 and 200.
        """
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        player = self.get_player(ctx)

        try:
            vol = float(arg)
        except ValueError:
            await ctx.send(f":loud_sound: The volume is currently set for **{player.volume * 100}%**.")
            usage.update(ctx)
            return ctx.command.name

        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            await ctx.send("I am not currently connected to a voice channel.")
            usage.update(ctx)
            return ctx.command.name

        if vol < 0:
            vol = 0
        elif vol > 200:
            vol = 200

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f":loud_sound: {ctx.author} set the volume to **{player.volume * 100}%**.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="loop", aliases=["repeat"])
    async def cmd_loop(self, ctx, arg=""):
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name
        player = self.players[ctx.guild.id]
        option = arg.lower().strip()
        options = {
            "on": True,
            "enable": True,
            "loop": True,
            "off": False,
            "disable": False,
            "noloop": False,
            "toggle": not player.loop_queue
        }
        current_queue = f"**{len(player.queue)}** songs {player.print_total_time()}"
        player.loop_queue = options.get(option, player.loop_queue)
        if player.loop_queue:
            title = f"🔁 Now looping {current_queue}"
            desc = f"To turn off looping, use `{ctx.prefix}loop off` or `{ctx.prefix}loop toggle`."
        else:
            title = f"▶️ Now playing (no loop) {current_queue}"
            desc = f"To turn on looping, use `{ctx.prefix}loop on` or `{ctx.prefix}loop toggle.`"
        e = discord.Embed(title=title, description=desc)
        await ctx.send(embed=e)
        usage.update(ctx, option)
        return ctx.command.name

    @commands.command(name="stop")
    async def cmd_stop(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            try:
                await ctx.guild.voice_client.disconnect()
            except AttributeError:
                pass
            await ctx.send(f"There are currently no songs queued. Want to start another jam session?\n\n _(Psst, use `{ctx.prefix}play`...)_")
            usage.update(ctx)
            return ctx.command.name

        await self.cleanup(ctx.guild)

        try:
            await ctx.guild.voice_client.disconnect()
        except AttributeError:
            pass

        usage.update(ctx)
        return ctx.command.name

    @commands.group(invoke_without_command=True, name="playlist", aliases=["pl", "playlists"])
    async def cmd_playlist(self, ctx, name=""):
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        with io.open("data/playlists.json") as f:
            playlist_data = json.load(f)
            if str(ctx.guild.id) not in playlist_data:
                await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
                usage.update(ctx)
                return ctx.command.name
            guild_pl = playlist_data[str(ctx.guild.id)]

            if name in guild_pl:
                playlist = guild_pl[name]
                desc = []
                full_duration = 0
                for i in range(0, math.ceil(len(playlist) / 20)):
                    desc.append("")
                for i in range(0, len(playlist)):
                    full_duration += playlist[i]["duration"]
                    line = f"{i + 1}. **{playlist[i]['title']}"
                    if len(line) > 100:
                        line = line[:97] + "..."
                    line += f"** {print_duration(playlist[i]['duration'])}\n"
                    desc[math.floor(i / 20)] += line
                for i in range(0, len(desc)):
                    e = discord.Embed(title=f"{name} Playlist for {ctx.guild.name} {print_duration(full_duration)}", description=desc[i])
                    e.set_footer(text=f"Page {i + 1}")
                    await ctx.send(embed=e)
                usage.update(ctx)
                return ctx.command.name

            title = f"**Playlists for {ctx.guild.name}**"
            desc = f"""
                Use `{ctx.prefix}playlist_name` to view `playlist_name`.\n
                Use `{ctx.prefix}load playlist_name` to load `playlist_name` onto the queue.\n
                Use `{ctx.prefix}save` to save up to the first 20 songs of the current queue as a playlist.\n
                Use `{ctx.prefix}pl remove` to remove a playlist.\n
                """
            playlists = []
            for name, queue in guild_pl.items():
                playlists.append((name[:100], len(queue)))

            for i in range(math.ceil(len(playlists) / 25)):
                e = discord.Embed(title=title, description=desc)
                e.set_footer(text=f"Page {i + 1}")
                for j in range(25):
                    try:
                        playlist = playlists[i + j]
                        e.add_field(name=playlist[0], value=f"{playlist[1]} song(s)")
                    except IndexError:
                        break
                await ctx.send(embed=e)

        usage.update(ctx)
        return ctx.command.name

    @cmd_playlist.command(name="remove", aliases=["rm", "delete", "del"])
    async def cmd_playlist_remove(self, ctx, arg=""):
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name
        # vc = ctx.voice_client

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        name = arg

        with io.open("data/playlists.json") as f:
            playlist_data = json.load(f)
            if str(ctx.guild.id) not in playlist_data:
                await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
                usage.update(ctx)
                return ctx.command.name
            guild_pl = playlist_data[str(ctx.guild.id)]

            if name == "":
                pl_list = ""
                for name, queue in guild_pl.items():
                    pl_list += f"`{name}`, "
                pl_list = (pl_list[:-2])[:1500]
                remove_message = f"{ctx.author.mention} Which playlist should be removed?\n{pl_list}\n(Type `cancel` to cancel the playlist removal.)"

                await ctx.send(remove_message)
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    name = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name

            if name not in guild_pl:
                await ctx.send(f"`{name}` is not a playlist for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to make it one!")
                usage.update(ctx)
                return ctx.command.name

            await ctx.send(f"{ctx.author.mention} Are you sure you want to delete `{name}`, a playlist with `{len(guild_pl[name])}` song(s)? (Y/N)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if "y" not in message.content.lower():
                    await ctx.send(f":x: {ctx.author.mention} `{name}` playlist is not removed.")
                    usage.update(ctx)
                    return ctx.command.name
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name

            del playlist_data[str(ctx.guild.id)][name]
            new_playlist_data = json.dumps(playlist_data, indent=4)
            with io.open("data/playlists.json", "w+") as fo:
                fo.write(new_playlist_data)

            await ctx.send(f":wastebasket: `{name}` playlist has been removed.")

        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="save", aliases=["export"])
    async def cmd_save(self, ctx, *, arg=""):
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name

        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            await ctx.send(f"There is currently no queue to save. Try queuing some songs with `{ctx.prefix}play`. :thinking:")
            usage.update(ctx)
            return ctx.command.name

        def check(message):
            return message.author == ctx.author and message.channel == ctx.channel
        name = arg

        if name == "":
            await ctx.send(f"{ctx.author.mention} What should the playlist name be?\n\n(Note: the playlist name may not contain spaces or line breaks. Type `cancel` to cancel the new playlist.)")
            try:
                message = await self.bot.wait_for("message", timeout=30.0, check=check)
                if message.content.lower() == "cancel":
                    await ctx.send(f":x: {ctx.author.mention} New playlist cancelled.")
                    usage.update(ctx)
                    return ctx.command.name
                name = message.content.strip().split()[0].strip()
            except asyncio.TimeoutError:
                await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                usage.update(ctx)
                return ctx.command.name

        new_playlist = []
        length = len(player.queue)
        if length > 20:
            length = 20
        for i in range(length):
            new_playlist.append(player.queue[i].to_dict())

        with io.open("data/playlists.json") as f:
            playlist_data = json.load(f)
            if str(ctx.guild.id) not in playlist_data:
                playlist_data[str(ctx.guild.id)] = {}
            if name in playlist_data[str(ctx.guild.id)]:
                await ctx.send(f"{ctx.author.mention} `{name}` is already a playlist name. Are you sure you want to overwrite this playlist? (Y/N)")
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    if "y" not in message.content.lower():
                        await ctx.send(f":x: {ctx.author.mention} New playlist cancelled.")
                        usage.update(ctx)
                        return ctx.command.name
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            playlist_data[str(ctx.guild.id)][name] = new_playlist
            new_playlist_data = json.dumps(playlist_data, indent=4)
            with io.open("data/playlists.json", "w+") as fo:
                fo.write(new_playlist_data)

        await ctx.send(f":white_check_mark: `{length}` song(s) in the current queue have been saved as playlist `{name}`.")

        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="load", aliases=["import"])
    async def cmd_load(self, ctx, name=""):
        in_channel = await self.is_in_channel(ctx)
        if not in_channel:
            usage.update(ctx)
            return ctx.command.name
        # vc = ctx.voice_client

        with io.open("data/playlists.json") as f:
            playlist_data = json.load(f)
            if str(ctx.guild.id) not in playlist_data:
                await ctx.send(f"No playlists were found for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to add some!")
                usage.update(ctx)
                return ctx.command.name
            guild_pl = playlist_data[str(ctx.guild.id)]

            if name not in guild_pl:
                await ctx.send(f"`{name}` is not a playlist for {ctx.guild.name}. Try queuing some songs and using `{ctx.prefix}save` to make it one!")
                usage.update(ctx)
                return ctx.command.name

            playlist = guild_pl[name]
            for i in range(len(playlist)):
                playlist[i] = YTInfo(playlist[i])

        await ctx.trigger_typing()

        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.cmd_connect)
        if ctx.guild.id not in ytdl:
            ytdl[ctx.guild.id] = YoutubeDL(get_ytdlopts(ctx.guild.id))
        player = self.get_player(ctx)
        if len(player.queue) == 0:
            player.queue = playlist
            await ctx.send(f":white_check_mark: `{len(playlist)}` song(s) from `{name}` loaded to the queue.")
        else:
            for song in playlist:
                player.queue.append(song)
            await ctx.send(f":white_check_mark: `{len(playlist)}` song(s) from `{name}` loaded to the queue.")
            usage.update(ctx)
            return ctx.command.name

        player.np = await YTDLSource.regather_stream(ctx, player.queue[0], loop=self.bot.loop)

        ctx.guild.voice_client.play(player.np, after=player.next_song)
        np = player.np
        e = discord.Embed(title=f"▶️ Now playing **{np.title}**.")
        e.add_field(name="Duration", value=print_duration(np.duration))
        e.add_field(name="Uploader", value=np.uploader)
        e.add_field(name="Upload Date", value=print_date(np.upload_date))
        await ctx.channel.send(embed=e)

        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Music(bot))
