"""
This is an example cog that shows how you would make use of Lavalink.py.
This example cog requires that you have python 3.6 or higher due to the f-strings.
"""
import math, re, io, json

import discord
import lavalink
from discord.ext import commands

from utils import lbvars, usage, lbutil
from preconditions import voice

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\\/\\/(?:www\\.)?.+')

class Music:
    slots = ("bot")
    
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):  # This ensures the client isn't overwritten during cog reloads.
            bot.lavalink = lavalink.Client(bot.user.id)
            bot.lavalink.add_node('159.65.238.124', 2333, lbvars.lavalinkpass, 'us', 'default-node')  # Host, Port, Password, Region, Name
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        bot.lavalink.add_event_hook(self.track_hook)

    def __unload(self):
        self.bot.lavalink._event_hooks.clear()

    async def track_hook(self, event):
        if isinstance(event, lavalink.events.TrackEndEvent):
            pass  # Send track ended message to channel.
        if isinstance(event, lavalink.events.TrackStartEvent):
            pass
            #TODO: Find a way to somehow record in what channel a player was started from and then use those events here.


    async def connect_to(self, guild_id: int, channel_id: str):
        """ Connects to the given voicechannel ID. A channel_id of `None` means disconnect. """
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command(name="play", aliases=['p'])
    @voice.isInVoiceChannel()
    @commands.guild_only()
    @voice.hasValidVoicePermissions()
    async def cmd_play(self, ctx, *, query: str):
        """ Searches and plays a song from a given query. """
        player = self.bot.lavalink.players.create(ctx.guild.id)
        should_connect = ctx.command.name in ('play')  # Add commands that require joining voice to work.

        if not player.is_connected:
            if not should_connect:
                raise commands.CommandInvokeError('Not connected.')
            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                raise ctx.send('You need to be in my voicechannel.')

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found!')

        embed = discord.Embed(color=discord.Color.blurple())

        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            await ctx.send(embed=embed)
        else:
            track = results['tracks'][0]
            embed.title = 'Track Enqueued'
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            await ctx.send(embed=embed)
            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

    @cmd_play.error
    async def play_error(self, ctx, error):
        if isinstance(error, voice.NotInVoiceChannel):
            e = discord.Embed(title="Command Error", description="You need to be in a voice channel to use this command")
            await ctx.send(embed=e)
        elif isinstance(error, voice.InvalidVoicePermissions):
            e = discord.Embed(title="Command Error", description="The bot requires `speak` and `connect` permissions in the voice channel you are in to play music.")
            await ctx.send(embed=e)
        elif isinstance(error, commands.NoPrivateMessage):
            e = discord.Embed(title="Command Error", description="Music is not supported in private messages")
            await ctx.send(embed=e)
        else:
            print("Unhandled error:" + str(error))

    @commands.command(name="skip", aliases=['forceskip'])
    async def cmd_skip(self, ctx):
        """ Skips the current track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        await player.skip()
        await ctx.send('⏭ | Skipped.')

    @commands.command(name="stop", aliases=['dc', 'disconnect'])
    async def cmd_stop(self, ctx):
        """ Stops the player and clears its queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if player is None:
            await self.connect_to(ctx.guild.id, None)
        else:
            if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
                return await ctx.send('You\'re not in my voicechannel!')
            if player.is_playing:
                player.queue.clear()
                await player.stop()
            await self.connect_to(ctx.guild.id, None)
            await ctx.send('⏹ | Stopped.')

    @commands.command(name="now", aliases=['np', 'n', 'playing'])
    async def cmd_now(self, ctx):
        """ Shows some stats about the currently playing song. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.current:
            return await ctx.send('Nothing playing.')

        position = lavalink.utils.format_time(player.position)
        if player.current.stream:
            duration = '🔴 LIVE'
        else:
            duration = lavalink.utils.format_time(player.current.duration)
        song = f'**[{player.current.title}]({player.current.uri})**\n({position}/{duration})'

        embed = discord.Embed(color=discord.Color.blurple(), title='Now Playing', description=song)
        await ctx.send(embed=embed)

    @commands.group(name="queue", aliases=['q'], invoke_without_command=True)
    async def cmd_queue(self, ctx, page: int = 1):
        """ Shows the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if player is None:
            embed = discord.Embed(color=discord.Color.blurple(), title="Nothing in queue", description="Want to add something? Use `lmao play <song name>`.")
            embed.set_footer(text="If you're looking to see what's currently playing, use `lmao np`")
            return await ctx.send(embed=embed)
            
        if not player.queue:
            embed = discord.Embed(color=discord.Color.blurple(), title="Nothing in queue", description="Want to add something? Use `lmao play <song name>`.")
            embed.set_footer(text="If you're looking to see what's currently playing, use `lmao np`")
            return await ctx.send(embed=embed)

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        queue_list = ''
        for index, track in enumerate(player.queue[start:end], start=start):
            queue_list += f'`{index + 1}.` [**{track.title}**]({track.uri})\n'

        embed = discord.Embed(colour=discord.Color.blurple(), description=f'**{len(player.queue)} tracks**\n\n{queue_list}')
        embed.set_footer(text=f'Viewing page {page}/{pages}')
        await ctx.send(embed=embed)

    @cmd_queue.command(name="remove", aliases=['rm', 'del', 'delete'])
    async def cmd_remove(self, ctx, index: int):
        """ Removes an item from the player's queue with the given index. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send('Nothing queued.')

        if index > len(player.queue) or index < 1:
            return await ctx.send(f'Index has to be **between** 1 and {len(player.queue)}')

        index -= 1
        removed = player.queue.pop(index)

        await ctx.send(f'Removed **{removed.title}** from the queue.')

    @commands.command(name="pause", aliases=['resume'])
    async def cmd_pause(self, ctx):
        """ Pauses/Resumes the current track. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Not playing.')

        if player.paused:
            await player.set_pause(False)
            await ctx.send('⏯ | Resumed')
        else:
            await player.set_pause(True)
            await ctx.send('⏯ | Paused')

    @commands.command(name="volume", aliases=['vol'])
    async def cmd_volume(self, ctx, volume: int = None):
        """ Changes the player's volume. Must be between 0 and 1000. Error Handling for that is done by Lavalink. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'🔈 | {player.volume}%')

        await player.set_volume(volume)
        await ctx.send(f'🔈 | Set to {player.volume}%')

    @commands.command(name="shuffle")
    async def cmd_shuffle(self, ctx):
        """ Shuffles the player's queue. """
        player = self.bot.lavalink.players.get(ctx.guild.id)
        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.shuffle = not player.shuffle
        await ctx.send('🔀 | Shuffle ' + ('enabled' if player.shuffle else 'disabled'))

    @commands.command(name="repeat", aliases=['loop'])
    async def cmd_repeat(self, ctx):
        """ Repeats the current song until the command is invoked again. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('Nothing playing.')

        player.repeat = not player.repeat
        await ctx.send('🔁 | Repeat ' + ('enabled' if player.repeat else 'disabled'))

    @commands.command(name="find", alises=['search'])
    async def cmd_find(self, ctx, *, query):
        """ Lists the first 10 search results from a given query. """
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('Nothing found')

        tracks = results['tracks'][:10]  # First 10 results

        o = ''
        for index, track in enumerate(tracks, start=1):
            track_title = track['info']['title']
            track_uri = track['info']['uri']
            o += f'`{index}.` [{track_title}]({track_uri})\n'

        embed = discord.Embed(color=discord.Color.blurple(), description=o)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Music(bot))