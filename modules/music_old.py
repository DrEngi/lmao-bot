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
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

client = discord.Client()

ytdlopts = {
    "format": "bestaudio/best",
    "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
    "restrictfilenames": True,
    "noplaylist": True,
    "nocheckcertificate": True,
    "ignoreerrors": False,
    "logtostderr": False,
    "quiet": True,
    "no_warnings": True,
    "default_search": "auto",
    "source_address": "0.0.0.0"  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    "before_options": "-nostdin",
    "options": "-vn"
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""

def print_duration(time):
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
        return "[{}:{}:{}]".format(h, m, s)
    else:
        return "[{}:{}]".format(m, s)
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

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        e = discord.Embed(title=f"✅ Added **{data['title']}** to the queue.")
        e.add_field(name="Duration", value=print_duration(data["duration"]))
        e.add_field(name="Uploader", value=data["uploader"])
        e.add_field(name="Upload Date", value=print_date(data["upload_date"]))
        e.set_footer(text=f"Requested by {ctx.author}")
        await ctx.send(embed=e)
        #await ctx.send(f"```ini\n[Added {data['title']} to the queue.]\n```")

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {"webpage_url": data["webpage_url"], "requester": ctx.author, "title": data["title"]}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data["requester"]

        to_run = partial(ytdl.extract_info, url=data["webpage_url"], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data["url"]), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice its instance will be destroyed.
    """

    __slots__ = ("bot", "_guild", "_channel", "_cog", "queue", "next", "current", "np", "volume")

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()
        # self.queue = []
        # self.next = []

        #self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def send_np(self):
        source = await self.queue.get()
        e = discord.Embed(title=f"▶️ Now playing **{source.title}**.")
        e.add_field(name="Duration", value=print_duration(source.duration))
        e.add_field(name="Uploader", value=source.uploader)
        e.add_field(name="Upload Date", value=print_date(source.upload_date))
        e.set_footer(text=f"Requested by {source.requester}")
        await self._channel.send(embed=e)

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f"There was an error processing your song.\n"
                                             f"```css\n[{e}]\n```")
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            #self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))

            e = discord.Embed(title=f"▶️ Now playing **{source.title}**.")
            e.add_field(name="Duration", value=print_duration(source.duration))
            e.add_field(name="Uploader", value=source.uploader)
            e.add_field(name="Upload Date", value=print_date(source.upload_date))
            e.set_footer(text=f"Requested by {source.requester}")
            await self._channel.send(embed=e)
            # await self.send_np()

            #self.np = await self._channel.send(f"**Now Playing:** `{source.title}` requested by "
            #                                   f"`{source.requester}`")
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

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

    @commands.command(name="connect", aliases=["join"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
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
            except AttributeError:
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
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="pause")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(f"There are no songs currently in the queue. Why not add some with `{ctx.prefix}play`? :thinking:")
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f"**`{ctx.author}`**: Paused the song!")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="resume")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"There are no songs currently in the queue. Maybe you should add some with {ctx.prefix}play... :thinking:")
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f"**`{ctx.author}`**: Resumed the song!")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="skip", aliases=["next"])
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"There are no songs currently in the queue. Try using `{ctx.prefix}play` to jam out to some tunes.")

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f"**`{ctx.author}`**: Skipped the song!")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="queue", aliases=["q", "playlist"])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to a voice channel.")

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(f"There are currently no queued songs. Use `{ctx.prefix}play` to start playing music!")

        # Grab up to 5 entries from the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        fmt = "\n".join(f"**`{_['title']}`**" for _ in upcoming)
        embed = discord.Embed(title=f"Upcoming - Next {len(upcoming)}", description=fmt)

        await ctx.send(embed=embed)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="now_playing", aliases=["np", "current", "currentsong", "playing"])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to voice!", delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send("I am not currently playing anything!")

        # try:
        #     # Remove our previous now_playing message.
        #     await player.np.delete()
        # except discord.HTTPException:
        #     pass

        # player.np = await ctx.send(f"**Now Playing:** `{vc.source.title}` "
        #                            f"requested by `{vc.source.requester}`")

        await ctx.send(f"**Now Playing:** `{vc.source.title}` "
                                   f"requested by `{vc.source.requester}`")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="volume", aliases=["vol"])
    async def change_volume(self, ctx, *, vol: float):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send("I am not currently connected to a voice channel.")

        if not 0 < vol < 101:
            return await ctx.send("Please enter a value between 1 and 100.")

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f"**`{ctx.author}`**: Set the volume to **{vol}%**.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="stop")
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(f"There are currently no songs queued. Want to start another jam session (psst, use `{ctx.prefix}play`)?")

        await self.cleanup(ctx.guild)
        usage.update(ctx)
        return ctx.command.name


def setup(bot):
    bot.add_cog(Music(bot))















# "play": cmd_play,
# "next": cmd_next,
# "skip": cmd_next,
# "pause": cmd_pause,
# "resume": cmd_resume,
# "stop": cmd_stop,
# "queue": cmd_queue,
# "q": cmd_queue,


# # Connects the bot to the voice channel the author is in; returns True if successful and False if not
# async def connect_voice():
#     global voice
#     if guild.voice_client != None:
#         return True
#     else:
#         if message.author.voice.channel != None:
#             voice[guild_id] = await message.author.voice.channel.connect()
#             return True
#         else:
#             await message.channel.send(mention + " You must be in a voice channel first.")
#             return False
# Disconnects the bot from voice channels in the current guild
# async def disconnect_voice():
#     for vc in bot.voice_clients:
#         if vc.guild == guild:
#             await vc.disconnect()
#             break
# # Given a time in seconds, returns [h:mm:ss]
# def video_duration(time):
#     t = lbutil.dhms_time(time)
#     h = t["h"] + 24 * t["d"]
#     m = str(t["m"])
#     s = str(t["s"])
#     if len(s) < 2:
#         s = "0" + s
#     m = str(m)
#     if len(m) < 2:
#         m = "0" + m
#     if h > 0:
#         return "[{}:{}:{}]".format(h, m, s)
#     else:
#         return "[{}:{}]".format(m, s)
# # Returns the video info in the form of Title [h:mm:ss], Title is not bold if bold=False
# def video_info(vid, bold=True):
#     bold_mark = "**"
#     if bold == False:
#         bold_mark = ""
#     title = vid.title[:180]
#     if title != vid.title:
#         title += "..."
#     return bold_mark + title + bold_mark + " " + video_duration(vid.duration)
# # After a song finishes playing, the player will automatically start playing the next song in the queue
# def next_song():
#     player[guild_id][0].stop()
#     player[guild_id].pop(0)
#     if len(player[guild_id]) > 0:
#         reload_song = voice[guild_id].create_ytdl_player(player[guild_id][0].url, after=next_song)
#         song = asyncio.run_coroutine_threadsafe(reload_song, bot.loop)
#         try:
#             player[guild_id][0] = song.result()
#             player[guild_id][0].start()
#         except Exception as e:
#             template = str(datetime.now()) + "Playing next song failed. Exception: {0}. Arguments:\n{1!r}"
#             print(template.format(type(e).__name__, e.args))
#             #pass
#         coro_msg = message.channel.send(":arrow_forward: Now playing {}.".format(video_info(player[guild_id][0])))
#     else:
#         coro_dc = disconnect_voice()
#         dc = asyncio.run_coroutine_threadsafe(coro_dc, bot.loop)
#         try:
#             dc.result()
#         except Exception as e:
#             template = str(datetime.now()) + "Disconnecting voice failed. Exception: {0}. Arguments:\n{1!r}"
#             print(template.format(type(e).__name__, e.args))
#             #pass
#         coro_msg = message.channel.send(":stop_button: The queue has finished.")
#     fut = asyncio.run_coroutine_threadsafe(coro_msg, bot.loop)
#     try:
#         fut.result()
#     except Exception as e:
#         template = str(datetime.now()) + "Message send failed. Exception: {0}. Arguments:\n{1!r}"
#         print(template.format(type(e).__name__, e.args))
#         #pass
# # Someone can add a new song to the queue, resume a paused song, or skip to a song later in the queue
# async def cmd_play():
#     if not discord.opus.is_loaded():
#         discord.opus.load_opus("libopus.so")
#     global player
#     connected = await connect_voice()
#     if connected:
#         await message.channel.trigger_typing()
#         if cmd_arg == "":
#             await cmd_resume()
#             return "play"
#         else:
#             skip = False
#             try:
#                 i = int(cmd_arg) - 1
#                 song_to_play = player[guild_id][i]
#                 player[guild_id].insert(1, song_to_play)
#                 player[guild_id].pop(i + 1)
#                 player[guild_id].insert(2, player[guild_id][0])
#                 player[guild_id][0].stop()
#                 skip = True
#             except (IndexError, ValueError) as e:
#                 try:
#                     player[guild_id].append(await voice[guild_id].create_ytdl_player(cmd_arg, after=next_song))
#                     await message.channel.send(":white_check_mark: Added {} to the queue.".format(video_info(player[guild_id][len(player[guild_id]) - 1])))
#                 except Exception as ex:
#                     template = str(datetime.now()) + "Not a URL. Exception: {0}. Arguments:\n{1!r}"
#                     print(template.format(type(ex).__name__, ex.args))
#                     try:
#                         player[guild_id].append(await voice[guild_id].create_ytdl_player("ytsearch:{" + cmd_arg + "}", after=next_song))
#                         await message.channel.send(":white_check_mark: Added {} to the queue.".format(video_info(player[guild_id][len(player[guild_id]) - 1])))
#                     except Exception as exc:
#                         template = str(datetime.now()) + "No song found. Exception: {0}. Arguments:\n{1!r}"
#                         print(template.format(type(exc).__name__, exc.args))
#                         await message.channel.send(":x: " + mention + " No results were found on YouTube for **{}**. Try searching for the video's URL.".format(cmd_arg))
#                         return "play"
#             if (len(player[guild_id]) == 1):
#                 await cmd_resume()
#             return "play"
# # Skips to the next song in the queue
# async def cmd_next():
#     global player
#     connected = await connect_voice()
#     if connected:
#         if len(player[guild_id]) < 1:
#             await message.channel.send(mention + " There are currently no songs in the queue.")
#         else:
#             player[guild_id][0].stop()
#             if (len(player[guild_id]) <= 0):
#                 await disconnect_voice()
#                 await message.channel.send(":stop_button: The queue has finished.")
#     return "next"
# # Pauses the current song in the queue
# async def cmd_pause():
#     connected = await connect_voice()
#     if connected:
#         if len(player[guild_id]) > 0:
#             player[guild_id][0].pause()
#             await message.channel.send(":pause_button: Paused {}. Use the `resume` command to resume.".format(video_info(player[guild_id][0])))
#         else:
#             await message.channel.send("There is nothing in the queue to pause.")
#         return "pause"
# # Resumes a paused song in the queue
# async def cmd_resume():
#     global player
#     global player_vol
#     if len(player[guild_id]) > 0:
#         try:
#             player[guild_id][0].start()
#             player[guild_id][0].pause()
#             player[guild_id][0] = await voice[guild_id].create_ytdl_player(player[guild_id][0].url, after=next_song)
#             player[guild_id][0].start()
#             #player[guild_id][0].volume = player_vol[guild_id]
#         except RuntimeError:
#             player[guild_id][0].resume()
#         await message.channel.send(":arrow_forward: Now playing {}.".format(video_info(player[guild_id][0])))
#     else:
#         await message.channel.send(mention + " There are currently no songs in the queue.")
#     return "resume"
# # Stops the queue
# async def cmd_stop():
#     connected = await connect_voice()
#     if connected:
#         if len(player[guild_id]) > 0:
#             player[guild_id][0].stop()
#             player[guild_id] = []
#             await message.channel.send(":stop_button: The queue has been stopped.")
#             await disconnect_voice()
#         else:
#             await message.channel.send(mention + " There are currently no songs in the queue.")
#             await disconnect_voice()
#     return "stop"
# # Lists the song in the queue and allows for people to add songs, remove songs, or clear the queue
# async def cmd_queue():
#     global player
#     q_cmd = cmd_arg.lower()
#     q_arg = ""
#     if cmd_arg.find(" ") != -1:
#         q_cmd = cmd_arg[:cmd_arg.find(" ")].lower()
#         q_arg = cmd_arg[cmd_arg.find(" ") + 1:]
#     if q_cmd == "add":
#         connected = await connect_voice()
#         if connected:
#             await message.channel.trigger_typing()
#             try:
#                 player[guild_id].append(await voice[guild_id].create_ytdl_player(q_arg, after=next_song))
#                 await message.channel.send(":white_check_mark: Added {} to the queue.".format(video_info(player[guild_id][len(player[guild_id]) - 1])))
#             except Exception as e:
#                 template = str(datetime.now()) + "Not a URL. Exception: {0}. Arguments:\n{1!r}"
#                 print(template.format(type(e).__name__, e.args))
#                 try:
#                     player[guild_id].append(await voice[guild_id].create_ytdl_player("ytsearch:{" + q_arg + "}", after=next_song))
#                     await message.channel.send(":white_check_mark: Added {} to the queue.".format(video_info(player[guild_id][len(player[guild_id]) - 1])))
#                 except Exception as ex:
#                     template = str(datetime.now()) + "No song found. Exception: {0}. Arguments:\n{1!r}"
#                     print(template.format(type(ex).__name__, ex.args))
#                     await message.channel.send(":x: " + mention + " No results were found on YouTube for **{}**. Try searching for the video's URL.".format(q_arg))
#         return "queue_add"
#     elif q_cmd == "remove":
#         connected = await connect_voice()
#         if connected:
#             try:
#                 i = int(q_arg) - 1
#                 if (i <= 0):
#                     await cmd_next()
#                 else:
#                     await message.channel.send(":wastebasket: {} has been removed from the queue.".format(video_info(player[guild_id][i])))
#                     player[guild_id].pop(i)
#             except ValueError:
#                 await message.channel.send(mention + " You must include the number of the song in the queue you want to remove. e.g. `" + prefix + " q remove 3`")
#             except IndexError:
#                 await message.channel.send(mention + " Song #{} does not exist in the queue.".format(i))
#         return "queue_remove"
#     elif q_cmd == "clear":
#         connected = await connect_voice()
#         if connected:
#             while(len(player[guild_id]) > 1):
#                 player[guild_id].pop(1)
#         await message.channel.send("The queue has been cleared.")
#         return "queue_clear"
#     else:
#         queue = []
#         if (len(player[guild_id]) == 0):
#             await message.channel.send("No songs are currently in queue.")
#             return "queue"
#         playtime = 0
#         for i in range(len(player[guild_id])):
#             queue.append("{}. {}\n".format(i + 1, video_info(player[guild_id][i], bold=False)))
#             playtime += player[guild_id][i].duration
#         playtime_str = video_duration(playtime)
#         queue_msg = "**SONGS CURRENTLY IN QUEUE** {}:\n\n".format(playtime_str)
#         while(True):
#             if len(queue) == 0:
#                 break
#             for i in range(10):
#                 if len(queue) == 0:
#                     break
#                 queue_msg += queue[0]
#                 queue.pop(0)
#             await message.channel.send(queue_msg)
#             queue_msg = ""
#         return "queue"
