import discord
from discord.ext import commands
from utils import lbvars, usage, lbutil, perms
import time
import io
import asyncio

class Info:

    slots = ("bot")

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", aliases=["helpme", "commands", "cmds"])
    async def cmd_help(self, ctx):   # DMs list of commands
        # Idea: Create objects instead of multiple lists
        if ctx.guild is None:
            prefix = "lmao "
        else:
            prefix = ctx.prefix
        await ctx.channel.trigger_typing()
        help_title = "🍑 **FULL LIST OF LMAO-BOT COMMANDS** 🍑"
        help_color = [
            0x008080,
            0xFF2500,
            0x3B88C3,
            0x0000FF,
            0xFFFF00,
            0x808080,
            0x008000,
            0xD11919,
            0xFBCEB1,
            0x666666
        ]
        help_head = [
                    "🤖 **Bot Management** 🤖",
                    "⚙️ **Lmao Message & Reaction Settings** ⚙️",
                    "🎵 **Music** 🎵",
                    "🚔 **Administration and Moderation** 🚔",
                    "🎉 **Fun Commands** 🎉",
                    "🛠️ **Utility** 🛠️",
                    "📊 **Probability Games & Commands** 📊",
                    "😏 **NSFW** 😏",
                    "✍️ **Custom Commands** ✍️",
                    "🔭 **Custom Filters** 🔭"
                    ]
        help_desc = [""":exclamation: `lmao prefix` If the bot's command prefix is not `lmao`, this returns the current command prefix.
                      \n:question: `{0}help` Returns a list of commands for lmao-bot to your DMs (hey, that's meta).
                      \n:computer: `{0}uptime` Shows how long lmao-bot has been up for as well as the time for the next maintenance break.
                      \n:ping_pong: `{0}ping` Sends the bot's latency (ping).
                      \n:exclamation: `{0}prefix` `new_prefix` Changes the bot's command prefix to `new_prefix`. Available to guild admins and lmao admins only. Default is "lmao".
                      \n:information_source: `{0}info` Gives a brief description about the bot, including an invite to the support server.
                      \n:incoming_envelope: `{0}invite` Need ass insurance in other guilds? Invite lmao-bot to other guilds you're in!
                      \n:information_desk_person: `{0}support` Sends an invite link to the lmao-bot support server.
                      \n:ballot_box: `{0}vote` Like lmao-bot? This gives you a link to vote for it on Discord Bot List!""",
                   """:peach: `{0}toggle` `chance` Changes the chance of automatic ass replacement after someone laughs their ass off to `chance` percent. Default is 100%.
                      \n:thumbsup: `{0}on` Changes the chance of automatic ass replacement to 100%.
                      \n:thumbsdown: `{0}off` Changes the chance of automatic ass replacement to 0%.
                      \n:slot_machine: `{0}lotto` Changes the chance of automatic ass replacement to 1% (spicy setting for spicy guilds).
                      \n:astonished: `{0}react` `chance` Changes the chance of emoji reaction features to `chance` percent. Default is 100%.
                      \n:chart_with_upwards_trend: `{0}chance` Returns the chance of automatic ass replacement and the chance of emoji reaction features.
                      \n:100: `{0}count` Counts the number of times you have used \"lmao\" or \"lmfao\".""",
                   """▶️ `{0}play` Plays the first song in the song queue.
                      \n▶️ `{0}play` `number` Plays song number `number` from the song queue.
                      \n▶️ `{0}play` `search_term` Plays the first result from a YouTube search for `search_term`.
                      \n▶️ `{0}play` `url` Plays music from a given URL `url`. Works with many video sites, including YouTube and Soundcloud.
                      \n🎤 `{0}connect` `voice_channel` Connects the bot to a voice channel named `voice_channel`. If `voice_channel` is not specified, the bot connects to the user's current voice channel.
                      \n▶️ `{0}nowplaying` or `{0}np` Shows information about the song currently playing.
                      \n⏭️ `{0}next` or `{0}skip` Ends the current song and plays the next song in the queue.
                      \n⏸️ `{0}pause` Pauses the current song.
                      \n⏯️ `{0}resume` Resumes a paused song.
                      \n🔊 `{0}volume` `percent` or `{0}vol` `percent` Changes the volume to `percent`%.
                      \n🔁 `{0}loop` Play the current queue on loop.
                      \n📻 `{0}queue` or `{0}q` Returns a list of all the songs in the queue.
                      \n➕ `{0}q` `add` `song` Adds a `song` (URL or search term) to the end of the queue.
                      \n➖ `{0}q` `remove` `number` Removes song number `number` from the queue.
                      \n🗑️ `{0}q` `clear` Clears the current queue.
                      \n📇 `{0}playlist` or `{0}pl` Shows the list of playlists.
                      \n🎶 `{0}pl` `playlist_name` Shows the songs in `playlist_name`.
                      \n🔖 `{0}save` Saves the current queue to a playlist.
                      \n🔂 `{0}load` `playlist_name` Loads `playlist_name` to the queue.
                      \n❌ `{0}pl` `remove` `playlist_name` Removes `playlist_name` from the list of playlists.""",
                   """:police_car: `{0}adminlist` Sends a list of everyone who is a lmao administrator.
                      \n:cop: `{0}addadmin` `member` Makes `member` a lmao administrator. Available to guild admins and existing lmao admins only.
                      \n:put_litter_in_its_place: `{0}removeadmin` `member` Removes `member` from the lmao administrator list. Available to guild admins only.
                      \n:wastebasket: `{0}purge` `num_of_messages` Purges (deletes) the most recent `num_of_messages` number of messages from the text channel.
                      \n:zipper_mouth: `{0}mute` `member` Prevents `member` from sending messages (mutes `member`) in a given text channel.
                      \n:zipper_mouth: `{0}mute` `time` `member` Mutes `member` in a given text channel for `time` (in minutes).
                      \n:open_mouth: `{0}unmute` `member` Allows `member` to send messages (unmutes `member`) in a given text channel.
                      \n:boot: `{0}kick` `member` `reason` Kicks `member` from the guild. `reason` is optional.
                      \n:hammer: `{0}ban` `member` `reason` Bans `member` from the guild. `reason` is optional.""",
                   """:loudspeaker: `{0}say` `message` Has lmao-bot say the `message` you want it to say.
                      \n:peach: `{0}booty` Sends a random SFW booty image in the chat.
                      \n:new_moon_with_face: `{0}moon` `member` Moons the mentioned `member`(s) with a SFW booty image.
                      \n:fire: `{0}deepfry` Deepfries an attached image, an image via URL, a mention user's profile picture, or one's own profile picture.
                      \n:princess: `{0}beautiful` `member` Lets a mentioned `member` know that they're beautiful with a frame from Gravity Falls.
                      \n:japanese_goblin: `{0}ugly` `member` Lets a mentioned `member` know that they're ugly with a frame from SpongeBob.
                      \n:wastebasket: `{0}garbage` `member` Lets a mentioned `member` know that they're garbage with a cute cartoon of a garbage can.
                      \n:rage: `{0}triggered` `member` Warns people to stay away from a mentioned `member`; they're triggered!.
                      \n:trophy: `{0}victory` `member` Displays to everyone `member`'s Victory Royale.
                      \n:cowboy: `{0}wanted` `member` Puts `member` on a WANTED poster.
                      \n:bust_in_silhouette: `{0}whosthat` `member` Who's that Pokémon? It's Pika-er... `member`?
                      \n:top: `{0}seenfromabove` `member` Voltorb? Pokéball? Electrode? Nope. It's `member`, seen from above.""",
                   """🖼️ `{0}avatar` `mention` Sends an image of the mentioned user's avatar.
                      \n❔ `{0}someone` `message` Pings a random person in the server with your message.
                      \n📙 `{0}urban` `term` Provides the definition for `term` on Urban Dictionary. Only works in NSFW channels.
                      \n🔍 `{0}lmgtfy` `what_to_google` Provides a nifty LMGTFY (Let Me Google That For You) link for `what_to_google`.
                      \n〰️ `{0}vaporwave` `text` Turns `text` into `ｔｅｘｔ`.
                      \n👏 `{0}clap` `message` 👏 Add 👏 some 👏 claps 👏 to 👏 your 👏 message. 👏
                      \n🎗️ `{0}remind` Sets up a reminder. After the amount of time you specify, you will be DM'd your reminder.
                      \n📅 `{0}reminders` Lists all your reminders.""",
                   """:moneybag: `{0}coin` `number_of_coins` Flips `number_of_coins` coins. If `number_of_coins` is not specified, one coin will be flipped.
                      \n:moneybag: `{0}flip` `number_of_coins` Does the same thing as `{0}coin`.
                      \n:game_die: `{0}dice` `number_of_dice` Rolls `number_of_dice` six-sided dice. If `number_of_dice` is not specified, one die will be rolled.
                      \n:game_die: `{0}roll` `number_of_dice` Does the same thing as `{0}dice`.
                      \n:black_joker: `{0}card` `number_of_cards` Draws `number_of_cards` cards (without replacement) from a standard 52-card deck. If `number_of_cards` is not specified, one card will be drawn.
                      \n:black_joker: `{0}draw` `number_of_cards` Does the same thing as `{0}card`.
                      \n:point_up_2: `{0}pick` `option1, option2, ...` Picks one option out of several given options, separated by commas.
                      \n:8ball: `{0}8ball` Provides a response from the Magic 8-Ball.
                      \n:thinking: `{0}guess start` Starts a number guessing game with a random number from 0 to 100.
                      \n:raising_hand: `{0}guess` `number` Guesses a `number` in an ongoing guessing game.
                      \n:flag_white: `{0}guess giveup` Gives up an ongoing guessing game. Only use this if you're a quitter.""",
                   """😳 `{0}nsfwtoggle` Toggles whether NSFW commands are allowed on the server or not.
                      \n🍑 `{0}ass` Sends a random NSFW ass picture.
                      \n🍈 `{0}boobs` Sends a random NSFW boobs picture.
                      \n🌮 `{0}pussy` Sends a random NSFW pussy picture.
                      \n🍆 `{0}dick` Sends a random NSFW dick picture.
                      \n🐙 `{0}hentai` Sends a random NSFW hentai GIF.
                      \n👩 `{0}gonewild` Sends a random post from the NSFW /r/gonewild subreddit.
                      \n👨 `{0}gonewildmale` Sends a random post from the NSFW /r/Ladybonersgw subreddit.
                      \n🧦 `{0}thighhighs` Sends a random post from the NSFW /r/thighhighs subreddit.
                      \n🖌️ `{0}rule34` `search_term` Sends a random NSFW Rule 34 post for `search_term`.
                      \n🖌️ `{0}r34` `search_term` Does the same thing as `{0}rule34`.""",
                   """:heavy_plus_sign: `{0}add` `command_name` `command_text` Adds `command_name` as a custom command, which prints `command_text` when executed.
                      \n:pencil: `{0}edit` `command_name` `command_text` Edits a certain command, `command_name`, to instead print `command_text` when executed.
                      \n:wastebasket: `{0}delete` `command_name` Deletes a certain command, `command_name`.
                      \n:clipboard: `{0}list` Lists all custom commands.
                      \n:speaking_head: `{0}command_name` Prints the message associated with the custom command `command_name`.""",
                   """🔭 `{0}filter` Lists all the custom filters for the guild.
                      \n➕ `{0}filter` `add` Adds a custom filter in the guild. When someone says a given word or phrase in a channel, lmao-bot automatically replies with a message.
                      \n✏️ `{0}filter` `edit` Edits a custom filter to say something else.
                      \n🚩 `{0}filter` `options` Change the options (flags) for a filter. Flags include `nomention`, `casesensitive`, `wholeword`, and `chance`.
                      \n🗑️ `{0}filter` `remove` Removes a custom filter."""]
        for i in range(len(help_head)):
            if "nsfw" in help_head[i].lower() and ctx.guild is not None and not lbvars.get_allow_nsfw(ctx.guild.id):
                continue
            e = discord.Embed(color=help_color[i], title=help_head[i], description=help_desc[i].format(prefix))
            if i > 0:
                await ctx.author.send(embed=e)
            else:
                await ctx.author.send(help_title, embed=e)
            await asyncio.sleep(0.1)
        if ctx.guild is not None:
            await ctx.send(f"{ctx.author.mention} A full list of lmao-bot commands has been slid into your DMs. :mailbox_with_mail:")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="prefix")
    async def cmd_prefix(self, ctx, *, arg=""):
        if perms.is_admin(ctx.message):
            new_prefix = arg
            if new_prefix == "":
                await ctx.send(f"{ctx.author.mention} My current prefix for {ctx.guild.name} is `{lbvars.get_prefix(ctx.guild.id)}`. What should I change it to?")
                def check(message):
                    return message.author == ctx.author and message.channel == ctx.channel
                try:
                    message = await self.bot.wait_for("message", timeout=30.0, check=check)
                    new_prefix = message.content
                except asyncio.TimeoutError:
                    await ctx.send(f":x: {ctx.author.mention} Command timed out.")
                    usage.update(ctx)
                    return ctx.command.name
            if "\n" in new_prefix:
                await ctx.send(f"{ctx.author.mention} Your command prefix may not contain line breaks.")
            elif len(new_prefix) > 20:
                await ctx.send(f"{ctx.author.mention} Your command prefix may not be longer than 20 characters.")
            else:
                lbvars.set_prefix(ctx.guild.id, new_prefix)
                await ctx.send(f"My command prefix for {ctx.guild.name} is now `{lbvars.get_prefix(ctx.guild.id)}`.")
        else:
            await ctx.send(f"{ctx.author.mention} You do not have the permission to change the bot's prefix. Ask a guild administrator or lmao administrator to do so.")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="uptime", aliases=["up"])
    async def cmd_uptime(self, ctx):
        current_time = time.time()
        with io.open("../management/next_maintenance.txt") as f:
            next_maintenance = f.read().strip()
        e = discord.Embed(color=lbvars.LMAO_ORANGE)
        e.add_field(name="lmao-bot Uptime", value=lbutil.eng_time(current_time - lbvars.start_time))
        e.add_field(name="Next Maintenance Break", value=next_maintenance)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="ping")
    async def cmd_ping(self, ctx):   # Ping-Pong
        pong_title = "🏓 Pong!"
        pong_desc = f"Latency: {round(self.bot.latency * 1000, 2)} ms"
        await ctx.send(embed=discord.Embed(title=pong_title, description=pong_desc))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="info", aliases=["about", "botinfo"])
    async def cmd_info(self, ctx):  # Returns about lmao-bot message
        desc = """I am a fun utility bot created by Firestar493#6963 and DrEngineer#8214 with discord.py in June 2018. I replace people's asses after they \"lmao\" or \"lmfao\". Try it out!\n
        I do all sorts of other things too, such as play music, provide moderation commands, and give answers from the almighty magic 8-ball. Invite me to one of your servers to see for yourself!"""
        e = discord.Embed(title="Hello from lmao-bot! 👋", color=lbvars.LMAO_ORANGE, description=desc)
        e.set_thumbnail(url=self.bot.user.avatar_url)
        e.add_field(name="Server Count", value=len(self.bot.guilds))
        e.add_field(name="Total Member Count", value=usage.count_total_members(self.bot))
        e.add_field(name="Shard Count", value=len(self.bot.shards))
        e.add_field(name="Invite me to your server", value="[You won't regret it 👀](https://discordapp.com/oauth2/authorize?client_id=459432854821142529&scope=bot&permissions=336063575)")
        e.add_field(name="Join the support server", value="[Send help pls](https://discord.gg/JQgB7p7)")
        e.add_field(name="Vote for me on Discord Bot List", value="[The power is in your hands](https://discordbots.org/bot/459432854821142529/vote)")
        e.set_footer(text="Try saying \"lmao help\" in a server I'm in!", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="support")
    async def cmd_support(self, ctx):
        await ctx.send("Need help with the bot? Don't worry, we've got your asses covered. Join the support server. :eyes:\n\nhttps://discord.gg/JQgB7p7")
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="invite")
    async def cmd_invite(self, ctx):
        invite_link = "https://discordapp.com/oauth2/authorize?client_id=459432854821142529&scope=bot&permissions=336063575"
        desc = f"Need ass insurance on other servers you're in?\n\n[Click here to invite me to more servers!]({invite_link})"
        e = discord.Embed(title="Invite lmao-bot!", color=lbvars.LMAO_ORANGE, description=desc)
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="vote", aliases=["upvote"])
    async def cmd_vote(self, ctx):
        vote_link = "https://discordbots.org/bot/459432854821142529/vote"
        desc = f"Like lmao-bot?\n\n[**Vote** for lmao-bot on Discord Bot List!]({vote_link})"
        e = discord.Embed(title="Vote for lmao-bot!", color=lbvars.LMAO_ORANGE, description=desc)
        e.set_thumbnail(url=self.bot.user.avatar_url)
        await ctx.send(embed=e)
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Info(bot))
