### TO-DO LIST ###
###REWRITE TO NEW DISCORD.PY LIBRARY

#lmao dadjoke: https://icanhazdadjoke.com/api
#lmao f: https://i.kym-cdn.com/entries/icons/mobile/000/017/039/pressf.jpg
    #alias: lmao rip: RIP mention. Press 'F' to pay respects. +:regional_indicator_f: reaction
#lmao clap: voice command, plays clap sound
#lmao boo: voice command, plays boo sound

#Add join/welcome message
#Add FAQ: lmao admins, command prefix, pronounce
#Server mute command
#Mute list + ban list
#Fix unmute glitch described in https://discordapp.com/channels/407274897350328345/461312988540829717/470635373161086977
    #Idea to fix: create a dictionary of "muted_until" with each server as a key and a list of muted members and times they should be unmuted as a value
    #If asyncio.sleep expires and time >= muted_until, unmute user
    #If asyncio.sleep expires and time < muted_until (due to multiple mutes being in place), don't unmute user
    #If user is ever unmuted, change muted_until to current time
#Import emojis from another server (lmao-bot server)
#CLEAN UP THIS MESS OF A 900+ LINE FILE
#Draw card feature - Two arrays, one of suits and the other of numbers, and prints number/letter + suit with emojis
    #Multiple draw feature - Max 52 cards, no substitution/repeats
    #Deal feature - allows mentioning users and dealing cards to each, no repeats  e.g. lmao deal 2 @User1 @User2 @User3
    #Shuffle
    #Deal faceup
    #Deal table
    #Discard
    #Play
#Pokemon data function; returns typing, abilities, stats, image; if pokemon name not found, return 'Pokemon not found. Make sure you include a valid Pokemon name after `lmao pokemon`.'; numbered array can sort each pokemon (e.g. all array index 1 will rep. Bulbasaur)
#List commands and command descriptions in an array/list
#Do dice rolls for dice other than 6-sided ones
#Check if server has no available channels to send messages in
#Change concatenated strings to .format
#Search for a specific channel to post announcements in
#Random custom command
#Aesthetic (a e s t h e t i c) command turns text into t e x t
#Birthday command - addbirthday, viewbirthday, and removebirthday - Says happy birthday if the date is someone's birthday and time is 12pm UTC; for loop for every day; maybe leap year birthdays celebrated on March 1

#lmao reset - resets lmao count

#Support server command

import discord
import asyncio
# import logging
import random
import io
import time
from datetime import datetime
import aiohttp
import socket
import json
import os
import lmaoutil as lu
import urban
import avatar
import lmgtfy
from PIL import Image

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

bot = discord.Client()

with io.open("tokens/token.txt", "r") as token:
    bot_token = (token.read())[:-1]
with io.open("tokens/dbl.txt", "r") as token:
    dbl_token = (token.read())[:-1]
dbl_url = "https://discordbots.org/api/bots/459432854821142529/stats"
dbl_headers = {"Authorization" : dbl_token}

### GLOBAL VARIABLES ###
start_time = time.time()    # Start time for lmao uptime command
cmd_prefix = {}             # Prefix for lmao-bot commands; default is "lmao "
lmao_admin_list = {}        # Dictionary for storing lmao admins
custom_cmd_list = {}        # Dictionary for storing custom commands.
replace_ass_chance = {}     # Chance of ass replacement
react_chance = {}           # Chance of ass reaction
magic_number = {}           # Magic number in number guessing game
guess_count = {}            # Number of guesses in number guessing game
deck = {}                   # TO BE WORKED ON: deck feature
init = []                   # Servers where settings have been initialized
server_count = 0
dm_count = 0
maintenance_time = "TBD"
voice = {}
player = {}
last_use_time = time.time()

ranks = [":regional_indicator_a:",
         ":two:",
         ":three:",
         ":four:",
         ":five:",
         ":six:",
         ":seven:",
         ":eight:",
         ":nine:",
         ":keycap_ten:",
         ":regional_indicator_j:",
         ":regional_indicator_q:",
         ":regional_indicator_k:"]
suits = [":clubs:",
         ":diamonds:",
         ":hearts:",
         ":spades:"]

# Updates usage stats
def update_usage(command_used):
    with io.open("cmd_usage.json") as f:
        cmd_usage_data = json.load(f)
        try:
            cmd_usage_data[command_used]["uses"] += 1
        except KeyError:
            cmd_usage_data[command_used] = {"uses": 1}
        new_cmd_data = json.dumps(cmd_usage_data, indent=4)
        with io.open("cmd_usage.json", "w+", encoding="utf-8") as fo:
            fo.write(new_cmd_data)

@bot.event
async def on_ready():   # Prints ready message in terminal
    global start_time
    start_time = time.time()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(str(datetime.now()))
    print('------')
    await bot.change_presence(game=discord.Game(name="lmao help | on {} servers | Firestar493#6963".format(len(bot.servers))))
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.servers)}
    # async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
    #     await aioclient.post(dbl_url, data=payload, headers=dbl_headers)
    #     dbl_connector.close()
    #     await aioclient.close()
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()
    await asyncio.sleep(60)
    while(True):
        await bot.change_presence(game=discord.Game(name="lmao help | Maint.: {} | Firestar493#6963".format(maintenance_time)))
        await asyncio.sleep(60)
        await bot.change_presence(game=discord.Game(name="lmao help | on {} servers | Firestar493#6963".format(len(bot.servers))))
        await asyncio.sleep(60)

@bot.event
async def on_server_join(server):
    print(str(datetime.now()) + " " + server.name + " just ADDED lmao-bot ^_^")
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.servers)}
    # async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
    #     await aioclient.post(dbl_url, data=payload, headers=dbl_headers)
    #     dbl_connector.close()
    #     await aioclient.close()
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()
    await asyncio.sleep(60)

@bot.event
async def on_server_remove(server):
    print(str(datetime.now()) + " " + server.name + " just REMOVED lmao-bot ;_;")
    dbl_connector = aiohttp.TCPConnector(family=socket.AF_INET,verify_ssl=False,force_close=True)
    payload = {"server_count"  : len(bot.servers)}
    # async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
    #     await aioclient.post(dbl_url, data=payload, headers=dbl_headers)
    #     dbl_connector.close()
    #     await aioclient.close()
    async with aiohttp.ClientSession(connector=dbl_connector) as aioclient:
        async with aioclient.post(dbl_url, data=payload, headers=dbl_headers) as r:
            dbl_connector.close()
            await aioclient.close()
    await asyncio.sleep(60)

@bot.event
async def on_member_join(member):
    if member.server.id == "463758816270483476":
        channel = member.server.get_channel("469491274219782144")
        await bot.send_typing(channel)
        beautiful = await avatar.beautiful(member)
        await bot.send_file(channel, "img/beautiful_{}.png".format(member.id), content="Welcome to {}, {}!".format(member.server.name, member.mention))

@bot.event
async def on_member_remove(member):
    if member.server.id == "463758816270483476":
        channel = member.server.get_channel("469491274219782144")
        await bot.send_message(channel, "Good night, sweet {}. You will be missed. :pensive:".format(str(member)))

@bot.event
async def on_message(message):  # Event triggers when message is sent
    channel = str(message.channel)
    author = str(message.author)
    author_dm = "Direct Message with " + author[:-5]
    try:
        perms = message.author.permissions_in(message.channel)
    except AttributeError:
        perms = discord.Permissions(permissions=0)
    if channel == author_dm:
        print(str(datetime.now()) + " DM from " + author + ": " + message.content)
    if channel == author_dm and author == r"Gucci Shawarma#6105": #r"Firestar493#6963":
        await bot.send_message(message.channel, "Hey, babe, what's up? :smirk:")

    server = message.server
    if server == None:
        server = message.channel
    server_id = server.id

    def shuffle_cards():
        global deck
        global ranks
        global suits
        deck[server_id] = []
        for rank in ranks:
            for suit in suits:
                deck[server_id].append([rank, suit])
        random.shuffle(deck[server_id])
    def import_settings():
        global cmd_prefix
        global replace_ass_chance
        global react_chance
        with io.open("settings.json") as f:
            settings_data = json.load(f)
            # if server_id not in settings_data.keys():
            #     cmd_prefix[server_id] = "lmao"
            #     replace_ass_chance[server_id] = 100
            #     react_chance[server_id] = 100
            # else:
            #     cmd_prefix[server_id] = settings_data[server_id]["cmd_prefix"].strip()
            #     replace_ass_chance[server_id] = settings_data[server_id]["replace_ass_chance"]
            #     react_chance[server_id] = settings_data[server_id]["react_chance"]
            try:
                cmd_prefix[server_id] = settings_data[server_id]["cmd_prefix"].strip()
            except KeyError:
                cmd_prefix[server_id] = "lmao"
            try:
                replace_ass_chance[server_id] = settings_data[server_id]["replace_ass_chance"]
            except KeyError:
                replace_ass_chance[server_id] = 100
            try:
                react_chance[server_id] = settings_data[server_id]["react_chance"]
            except KeyError:
                react_chance[server_id] = 100
    def import_admins():
        global lmao_admin_list
        with io.open("admins.json") as f:
            admins_data = json.load(f)
            if server_id not in admins_data.keys():
                lmao_admin_list[server_id] = []
            else:
                lmao_admin_list[server_id] = admins_data[server_id]
    def export_admins():
        with io.open("admins.json") as f:
            new_admins_data = json.dumps(lmao_admin_list, indent=4)
            with io.open("admins.json", "w+", encoding="utf-8") as fo:
                fo.write(new_admins_data)

    global init
    if server_id not in init:
        global cmd_prefix
        global lmao_admin_list
        global custom_cmd_list
        global replace_ass_chance
        global react_chance
        global magic_number
        global guess_count
        global server_count
        global dm_count
        global voice
        global player

        import_settings()
        import_admins()
        # if server_id not in lmao_admin_list.keys():
        #     lmao_admin_list[server_id] = []

        magic_number[server_id] = -1
        guess_count[server_id] = 0
        voice[server_id] = None
        player[server_id] = []
        shuffle_cards()
        if message.server == None:
            dm_count += 1
            print(str(datetime.now()) + " " + "{} initialized. DM count: {}.".format(str(message.author), dm_count))
        else:
            server_count += 1
            print(str(datetime.now()) + " " + "{} initialized. Server count: {}.".format(message.server.name, server_count))
        init.append(server_id)

    lmao_admin = perms.administrator or message.author.id in lmao_admin_list[server_id] or message.author.id == "210220782012334081"

    # If used by bot's creator, displays last time a lmao-bot command was used
    if message.author.id == "210220782012334081" and message.content.lower().strip() == "last command used":
        current_time = time.time()
        await bot.send_message(message.channel, "The last command was used " + lu.eng_time(current_time - last_use_time) + " ago.")

    # Prevent the bot from activating its own commands
    #if message.author == bot.user:
    if message.author.bot:
        return

    prefix = cmd_prefix[server_id]
    msg_raw = message.content
    msg = msg_raw.lower()
    cmd_raw = msg_raw[len(prefix):]
    cmd = cmd_raw.lower() # The command that lmao-bot responds to when called
    mention = message.author.mention
    replace_ass_msg = mention + ' You appear to have misplaced your ass while laughing. Here is a replacement: :peach:'

    async def replace_ass():    # Sends the ass substitution message
        with io.open("user_data.json") as f:
            lmao_count_data = json.load(f)
            try:
                lmao_count_data[message.author.id]["lmao_count"] += 1
            except KeyError:
                lmao_count_data[message.author.id] = {"lmao_count": 1}
            lmao_count_data[message.author.id]["username"] = str(message.author)
            new_user_data = json.dumps(lmao_count_data, indent=4)
            with io.open("user_data.json", "w+", encoding="utf-8") as fo:
                fo.write(new_user_data)
        x = random.randint(1, 100)
        global react_chance
        if x <= react_chance[server_id]:
            await bot.add_reaction(message, '🍑')
        y = random.randint(1, 100)
        global replace_ass_chance
        if y <= replace_ass_chance[server_id]:
            await bot.send_message(message.channel, replace_ass_msg)

    global custom_cmd_list
    async def import_customs():
        global custom_cmd_list
        with io.open("customs.json") as f:
            custom_cmd_list = json.load(f)
    async def export_customs():
        with io.open("customs.json") as f:
            new_customs_data = json.dumps(custom_cmd_list, indent=4)
            with io.open("customs.json", "w+", encoding="utf-8") as fo:
                fo.write(new_customs_data)

    # COMMANDS
    if msg.startswith(prefix.lower()): # Bot reacts to command prefix call
        space_ind = cmd.strip().find(' ')
        cmd_word = cmd.strip()
        cmd_arg = ""
        if space_ind != -1:
            cmd_word = cmd.strip()[:space_ind]
            cmd_arg = cmd_raw.strip()[space_ind+1:]
        import_admins()
        await import_customs()
        async def cmd_switch(command):
            async def cmd_announce():
                if message.author.id == "210220782012334081":
                    server_list = []
                    for server_x in bot.servers:
                        server_list.append(server_x)
                    for server_x in server_list:
                        channel_list = []
                        for channel_x in server_x.channels:
                            channel_list.append(channel_x)
                        announced = False
                        for channel_x in channel_list:
                            try:
                                if channel_x.permissions_for(server_x.me).send_messages and str(channel_x.type) == "text" and channel_x.is_default:
                                    with io.open("announcement_finished.txt", "a") as f:
                                        f.write("{} ({})".format(server_x.name, server_x.id))
                                    await bot.send_message(channel_x, cmd_arg)
                                    announced = True
                                    break
                            except AttributeError:
                                pass
                            except discord.errors.Forbidden:
                                pass
                            if not announced:
                                try:
                                    if channel_x.permissions_for(server_x.me).send_messages and str(channel_x.type) == "text":
                                        with io.open("announcement_finished.txt", "a") as f:
                                            f.write("{} ({})".format(server_x.name, server_x.id))
                                        await bot.send_message(channel_x, cmd_arg)
                                        break
                                except AttributeError:
                                    pass
                                except discord.errors.Forbidden:
                                    pass
                        await asyncio.sleep(10)
                else:
                    await replace_ass()
                return 'announce'
            async def cmd_change_maintenance():
                if message.author.id == "210220782012334081":
                    global maintenance_time
                    maintenance_time = cmd_arg
                    await bot.change_presence(game=discord.Game(name=r'lmao help | Maint.: {} | Firestar493#6963'.format(maintenance_time)))
                return 'change_maintenance'
            async def cmd_change_game():
                if message.author.id == "210220782012334081":
                    await bot.change_presence(game=discord.Game(name=cmd_arg))
                return 'change_game'
            async def cmd_uptime():
                current_time = time.time()
                with io.open("next_maintenance.txt") as f:
                    next_maintenance = f.read().strip()
                await bot.send_message(message.channel, "lmao-bot has been up for {}\n\nNext maintenance break is scheduled for {}.".format(lu.eng_time(current_time - start_time), next_maintenance))
                return 'uptime'
            async def cmd_toggle_ass(): # Toggle whether automatic ass substitution happens or not
                if lmao_admin or perms.manage_messages:
                    global replace_ass_chance
                    valid_chance = True
                    chance = replace_ass_chance[server_id]
                    try:
                        chance = int(cmd_arg)
                        if chance < 0 or chance > 100:
                            valid_chance = False
                    except ValueError:
                        if cmd_arg == "off" or cmd_word == "off":
                            chance = 0
                        elif cmd_arg == "on" or cmd_word == "on":
                            chance = 100
                        elif cmd_word == "lotto":
                            chance = 1
                        else:
                            valid_chance = False
                    if valid_chance:
                        after_msg = ""
                        if chance <= 50:
                            after_msg = "Tread carefully, and hold onto your buns."
                        else:
                            after_msg = "Don't do anything reckless; you'll be fine."
                        replace_ass_chance[server_id] = chance
                        await bot.send_message(message.channel, r'You have changed the automatic ass replacement chance to ' + str(replace_ass_chance[server_id]) + r"%. " + after_msg)
                    else:
                        await bot.send_message(message.channel, r'You must include an integer after toggleass from 0 to 100. This is the chance (in %) of automatic ass replacement.')
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to change the ass replacement chance. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                return 'toggle_ass'
            async def cmd_react():
                if lmao_admin or perms.manage_messages:
                    global react_chance
                    valid_chance = True
                    chance = react_chance[server_id]
                    try:
                        chance = int(cmd_arg)
                        if chance < 0 or chance > 100:
                            valid_chance = False
                    except ValueError:
                        if cmd_arg == "off":
                            chance = 0
                        elif cmd_arg == "on":
                            chance = 100
                        else:
                            valid_chance = False
                    if valid_chance:
                        after_msg = ""
                        if chance == 0:
                            after_msg = "Looks like the Fine Bros found us. :pensive:"
                        else:
                            after_msg = "Watch out for the Fine Bros. :eyes:"
                        react_chance[server_id] = chance
                        await bot.send_message(message.channel, r'You have changed the automatic emoji reaction chance to ' + str(react_chance[server_id]) + r"%. " + after_msg)
                    else:
                        await bot.send_message(message.channel, r'You must include an integer after `react` from 0 to 100. This is the chance (in %) of automatic emoji reactions.')
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to change the reaction chance. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                return 'react'
            async def cmd_chance():
                await bot.send_message(message.channel, "Ass replacement chance: **" + str(replace_ass_chance[server_id]) + "%**\nAss reaction chance: **" + str(react_chance[server_id]) + "%**")
                return 'chance'
            async def cmd_help():   # DMs list of commands
                await bot.send_typing(message.channel)
                dm_help = [""":peach: **FULL LIST OF LMAO-BOT COMMANDS** :peach:
                              \n
                              \n:robot: **Bot Management** :robot:
                              \n:exclamation: `lmao prefix` If the bot's command prefix is not `lmao`, this returns the current command prefix.
                              \n:question: `{0}help` Returns a list of commands for lmao-bot to your DMs (hey, that's meta).
                              \n:computer: `{0}uptime` Shows how long lmao-bot has been up for as well as the time for the next maintenance break.
                              \n:ping_pong: `{0}ping` Returns \"pong\".
                              \n:exclamation: `{0}prefix` `new_prefix` Changes the bot's command prefix to `new_prefix`. Available to server admins and lmao admins only. Default is "lmao ".
                              \n:information_source: `{0}about` Gives a brief description about the bot, including an invite to the support server.
                              \n:incoming_envelope: `{0}invite` Need ass insurance in other servers? Invite lmao-bot to other servers you're in!
                              \n:information_desk_person: `{0}support` Sends an invite link to the lmao-bot support server.
                              \n:ballot_box: `{0}vote` Like lmao-bot? This gives you a link to vote for it on Discord Bot List!""",
                           """_ _\n
                              \n:gear: **Lmao Message & Reaction Settings** :gear:
                              \n:peach: `{0}toggleass` `chance` Changes the chance of automatic ass replacement after someone laughs their ass off to `chance` percent. Default is 100%.
                              \n:peach: `{0}asstoggle` `chance` Does the same thing as `{0}toggleass`.
                              \n:thumbsup: `{0}on` Changes the chance of automatic ass replacement to 100%.
                              \n:thumbsdown: `{0}off` Changes the chance of automatic ass replacement to 0%.
                              \n:slot_machine: `{0}lotto` Changes the chance of automatic ass replacement to 1% (spicy setting for spicy servers).
                              \n:astonished: `{0}react` `chance` Changes the chance of emoji reaction features to `chance` percent. Default is 100%.
                              \n:chart_with_upwards_trend: `{0}chance` Returns the chance of automatic ass replacement and the chance of emoji reaction features.
                              \n:100: `{0}count` Counts the number of times you have used \"lmao\" or \"lmfao\".""",
                           """_ _\n
                              \n:musical_note: **Music** :musical_note:
                              \n:arrow_forward: `{0}play` Plays the first song in the song queue.
                              \n:arrow_forward: `{0}play` `number` Plays song number `number` from the song queue.
                              \n:arrow_forward: `{0}play` `search_term` Plays the first result from a YouTube search for `search_term`.
                              \n:arrow_forward: `{0}play` `url` Plays music from a given URL `url`. Works with many video sites, including YouTube and Soundcloud.
                              \n:fast_forward: `{0}next` Ends the current song and plays the next song in the queue.
                              \n:fast_forward: `{0}skip` Does the same thing as `{0}next`.
                              \n:pause_button: `{0}pause` Pauses the current song.
                              \n:play_pause: `{0}resume` Resumes a paused song.
                              \n:radio: `{0}queue` Returns a list of all the songs in the queue.
                              \n:radio: `{0}q` Does the same thing as `{0}queue`.
                              \n:heavy_plus_sign: `{0}q` `add` `song` Adds a `song` (URL or search term) to the end of the queue.
                              \n:heavy_minus_sign: `{0}q` `remove` `number` Removes song number `number` from the queue.
                              \n:wastebasket: `{0}q` `clear` Clears the current queue.""",
                           """_ _\n
                              \n:oncoming_police_car: **Administration and Moderation** :oncoming_police_car:
                              \n:police_car: `{0}adminlist` Sends a list of everyone who is a lmao administrator.
                              \n:cop: `{0}addadmin` `member` Makes `member` a lmao administrator. Available to server admins and existing lmao admins only.
                              \n:put_litter_in_its_place: `{0}removeadmin` `member` Removes `member` from the lmao administrator list. Available to server admins only.
                              \n:wastebasket: `{0}purge` `num_of_messages` Purges (deletes) the most recent `num_of_messages` number of messages from the text channel.
                              \n:zipper_mouth: `{0}mute` `member` Prevents `member` from sending messages (mutes `member`) in a given text channel.
                              \n:zipper_mouth: `{0}mute` `time` `member` Mutes `member` in a given text channel for `time` (in minutes).
                              \n:open_mouth: `{0}unmute` `member` Allows `member` to send messages (unmutes `member`) in a given text channel.
                              \n:boot: `{0}kick` `member` Kicks `member` from the server.
                              \n:hammer: `{0}ban` `member` Bans `member` from the server.""",
                           """_ _\n
                              \n:tada: **Fun Commands** :tada:
                              \n:loudspeaker: `{0}say` `message` Has lmao-bot say the `message` you want it to say.
                              \n:peach: `{0}booty` Sends a random SFW booty image in the chat.
                              \n:new_moon_with_face: `{0}moon` `member` Moons the mentioned `member`(s) with a SFW booty image.
                              \n:princess: `{0}beautiful` `member` Lets a mentioned `member` know that they're beautiful with a frame from Gravity Falls.
                              \n:japanese_goblin: `{0}ugly` `member` Lets a mentioned `member` know that they're ugly with a frame from SpongeBob.
                              \n:rage: `{0}triggered` `member` Warns people to stay away from a mentioned `member`; they're triggered!.
                              \n:trophy: `{0}victory` `member` Displays to everyone `member`'s Victory Royale.
                              \n:cowboy: `{0}wanted` `member` Puts `member` on a WANTED poster.
                              \n:bust_in_silhouette: `{0}whosthat` `member` Who's that Pokémon? It's Pika-er... `member`?
                              \n:top: `{0}seenfromabove` `member` Voltorb? Pokéball? Electrode? Nope. It's `member`, seen from above.
                              \n
                              \n:tools: **Utility** :tools:
                              \n:orange_book: `{0}urban` `term` Provides the definition for `term` on Urban Dictionary. Not yet available.
                              \n:mag: `{0}lmgtfy` `what_to_google` Provides a nifty LMGTFY (Let Me Google That For You) link for `what_to_google`.""",
                           """_ _\n
                              \n:bar_chart: **Probability Games & Commands** :bar_chart:
                              \n:moneybag: `{0}coin` `number_of_coins` Flips `number_of_coins` coins. If `number_of_coins` is not specified, one coin will be flipped.
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
                           """_ _\n
                              \n:writing_hand: **Custom Commands** :writing_hand:
                              \n:heavy_plus_sign: `{0}add` `command_name` `command_text` Adds `command_name` as a custom command, which prints `command_text` when executed.
                              \n:pencil: `{0}edit` `command_name` `command_text` Edits a certain command, `command_name`, to instead print `command_text` when executed.
                              \n:wastebasket: `{0}delete` `command_name` Deletes a certain command, `command_name`.
                              \n:clipboard: `{0}list` Lists all custom commands.
                              \n:speaking_head: `{0}command_name` Prints the message associated with the custom command `command_name`."""]
                              #\n
                              #\n**About lmao-bot**: lmao-bot was created by Firestar493#6963 in June 2018 as a fun Discord bot for replacing people's asses after they \"lmao\" or \"lmfao\". The bot is written in Python using the discord.py library, and the support server is https://discord.gg/JQgB7p7."""
                for msg_part in dm_help:
                    await bot.send_message(message.author, msg_part.format(prefix + " "))
                    #await asyncio.sleep(1)
                await bot.send_message(message.channel, mention + ' A full list of lmao-bot commands has been slid into your DMs. :mailbox_with_mail:')
                return 'help'
            async def cmd_count():  # Counts the number of times someone says lmao
                with io.open("user_data.json") as f:
                    lmao_count_data = json.load(f)
                    try:
                        await bot.send_message(message.channel, mention + " You have laughed your ass off {} times.".format(lmao_count_data[message.author.id]["lmao_count"]))
                    except KeyError:
                        await bot.send_message(message.channel, mention + " You have yet to laugh your ass off.")
                return 'count'
            async def cmd_ping():   # Ping-Pong
                await bot.send_message(message.channel, ':ping_pong: Pong')
                return 'ping'
            async def cmd_prefix():
                global cmd_prefix
                if lmao_admin:
                    if cmd_arg == "":
                        await bot.send_message(message.channel, "To update the command prefix, type `" + prefix + " prefix` `new_prefix`, where new_prefix is your new prefix.")
                    #elif cmd_arg[0:1] != "\"" or cmd_arg[-1:len(cmd_arg)] != "\"":
                    #    await bot.send_message(message.channel, "You must surround your new prefix with quotation marks to change the prefix. e.g. `" + prefix + " prefix \"new_prefix\"`.")
                    elif "\n" in cmd_arg:
                        await bot.send_message(message.channel, "Your command prefix may not contain line breaks.")
                    elif len(cmd_arg) > 20:
                        await bot.send_message(message.channel, "Your command prefix may not be longer than 20 characters.")
                    else:
                        cmd_prefix[server_id] = cmd_arg
                        await bot.send_message(message.channel, "The prefix for lmao-bot is now `" + cmd_prefix[server_id] + "`.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to change the bot's prefix. Ask a server administrator or lmao administrator to do so.")
                return 'prefix'
            async def cmd_about():  # Returns about lmao-bot message
                await bot.send_message(message.channel, """**About lmao-bot**: lmao-bot was created by Firestar493#6963 in June 2018 as a fun Discord bot for replacing people's asses after they \"lmao\" or \"lmfao\". The bot is written in Python using the discord.py library, and the support server is <https://discord.gg/JQgB7p7>.
                    \n\nlmao-bot is currently replacing asses on **{}** servers.
                    \n\nLike lmao-bot? **Vote** for lmao-bot on Discord Bot List! <https://discordbots.org/bot/459432854821142529/vote>""".format(len(bot.servers)))
                return 'about'
            async def cmd_support():
                await bot.send_message(message.channel, "Need help with the bot? Don't worry, we've got your asses covered. Join the support server. :eyes:\n\nhttps://discord.gg/JQgB7p7")
                return 'invite'
            async def cmd_invite():
                await bot.send_message(message.channel, "Need ass insurance in other servers you're in?\n\nInvite me to more servers! https://discordapp.com/oauth2/authorize?client_id=459432854821142529&scope=bot&permissions=336063575")
                return 'invite'
            async def cmd_vote():
                await bot.send_message(message.channel, "Like lmao-bot? **Vote** for lmao-bot on Discord Bot List!\n\nhttps://discordbots.org/bot/459432854821142529/vote")
                return 'vote'
            async def cmd_say():    # Allows user to have lmao-bot say a message
                if cmd_arg == "":
                    await bot.send_message(message.channel, 'You have to have a message for me to say. e.g. `" + prefix + " say Replacing asses by day, kicking asses by night.`')
                else:
                    try:
                        await bot.delete_message(message)
                    except discord.errors.Forbidden:
                        pass
                    except discord.errors.NotFound:
                        pass
                    await bot.send_message(message.channel, cmd_arg)
                return 'say'
            async def cmd_admin_list():
                global lmao_admin_list
                admin_list = "**Full list of lmao administrators for this server:**\n\n"
                for admin in lmao_admin_list[server_id]:
                    admin_list += server.get_member(admin).name + "\n"
                for i in range(0, len(admin_list), 2000):
                    await bot.send_message(message.channel, admin_list[i:i+2000])
                return 'admin_list'
            async def cmd_add_admin():
                global lmao_admin_list
                if lmao_admin:
                    if len(message.mentions) == 1:
                        if message.mentions[0].id in lmao_admin_list[server_id]:
                            await bot.send_message(message.channel, message.mentions[0].name + " is already a lmao administrator.")
                        else:
                            lmao_admin_list[server_id].append(message.mentions[0].id)
                            await bot.send_message(message.channel, message.mentions[0].mention + " has been added as a lmao administrator for this server.")
                    elif len(message.mentions) > 1:
                        await bot.send_message(message.channel, mention + " You may only add one lmao administrator at a time.")
                    elif len(message.mentions) < 1:
                        await bot.send_message(message.channel, mention + " You must mention the user you want to add as a lmao administrator.")
                else:
                    await bot.send_message(message.channel, mention + " Only server administrators and lmao administrators can add other lmao administrators.")
                return 'add_admin'
            async def cmd_remove_admin():
                global lmao_admin_list
                if perms.administrator:
                    if len(message.mentions) == 1:
                        if message.mentions[0].id not in lmao_admin_list[server_id]:
                            await bot.send_message(message.channel, message.mentions[0].name + " is not a lmao administrator.")
                        else:
                            lmao_admin_list[server_id] = [admin for admin in lmao_admin_list[server_id] if admin != message.mentions[0].id]
                            await bot.send_message(message.channel, message.mentions[0].mention + " has been removed as a lmao administrator for this server.")
                    elif len(message.mentions) > 1:
                        await bot.send_message(message.channel, mention + " You may only remove one lmao administrator at a time.")
                    elif len(message.mentions) < 1:
                        await bot.send_message(message.channel, mention + " You must mention the user you want to remove as a lmao administrator.")
                else:
                    await bot.send_message(message.channel, mention + " Only server administrators can remove lmao administrators.")
                return 'remove_admin'
            async def cmd_purge():  # Allows the deletion of messages
                if perms.manage_messages:
                    try:
                        if int(cmd_arg) > 100:
                            await bot.send_message(message.channel, "You cannot delete more than 100 messages.")
                        elif int(cmd_arg) > 0:
                            deleted = await bot.purge_from(message.channel, limit=int(cmd_arg) + 1)
                            deleted_message = await bot.send_message(message.channel, "**Successfully deleted {} message(s).**".format(len(deleted) - 1))
                            await asyncio.sleep(3)
                            await bot.delete_message(deleted_message)
                        elif int(cmd_arg) == 0:
                            await bot.send_message(message.channel, mention + " I'm always deleting 0 messages. You don't need to call a command for that.")
                        else:
                            await bot.send_message(message.channel, mention + " What, you think I'm some sort of magician who can delete a negative number of messages?")
                    except ValueError:
                        await bot.send_message(message.channel, mention + " You must specify the number of messages to purge. e.g. `" + prefix + " purge 5`")
                    except discord.errors.Forbidden:
                        await bot.send_message(message.channel, mention + " The messages could not be purged due to insufficient permissions for lmao-bot. Make sure `Manage Messages` is enabled for lmao-bot.")
                    return 'purge'
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to manage messages.")
                    return 'purge'
            async def cmd_mute():
                #muted_perms = discord.Permissions(send_messages=False)
                #lmao_muted = await bot.create_role(message.server, name="lmao muted", permissions=muted_perms)
                if perms.manage_channels:
                    try:
                        if len(message.mentions) == 1:
                            if message.mentions[0] == bot.user:
                                await bot.send_message(message.channel, "Silly " + mention + ", I can't mute myself!")
                            elif message.mentions[0].id == "210220782012334081":
                                await bot.send_message(message.channel, "Please, " + mention + ", you can't mute my creator.")
                            else:
                                mute_time = 0
                                if cmd_arg.find(' ') != -1:
                                    try:
                                        mute_time = int(cmd_arg[:cmd_arg.find(' ')])
                                        if mute_time <= 0:
                                            mute_time = 0
                                    except ValueError:
                                        mute_time = 0
                                muted_perms = message.channel.overwrites_for(message.mentions[0])
                                muted_perms.send_messages = False
                                await bot.edit_channel_permissions(message.channel, message.mentions[0], muted_perms)
                                #await bot.add_roles(message.mentions[0], lmao_muted)
                                after_msg = ""
                                if mute_time != 0:
                                    after_msg += " for {} minutes".format(str(mute_time))
                                after_msg += "."
                                await bot.send_message(message.channel, message.mentions[0].mention + " was muted in " + message.channel.mention + " by " + message.author.mention + after_msg)
                                if mute_time != 0:
                                    await asyncio.sleep(mute_time * 60)
                                    muted_perms = message.channel.overwrites_for(message.mentions[0])
                                    muted_perms.send_messages = None
                                    await bot.edit_channel_permissions(message.channel, message.mentions[0], muted_perms)
                        elif len(message.mentions) < 1:
                            await bot.send_message(message.channel, mention + " You must mention the user you want to mute on this channel.")
                        elif len(message.mentions) > 1:
                            await bot.send_message(message.channel, mention + " You may not mute more than one member at a time.")
                    except discord.errors.Forbidden:
                        await bot.send_message(message.channel, mention + " lmao-bot eithers lacks the permission to mute members or the member you tried to mute is of an equal or higher role than lmao-bot. Make sure `Manage Channels` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to mute.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to mute members.")
                return 'mute'
            async def cmd_unmute():
                if perms.manage_channels:
                    try:
                        if len(message.mentions) == 1:
                            unmuted_perms = message.channel.overwrites_for(message.mentions[0])
                            unmuted_perms.send_messages = None
                            await bot.edit_channel_permissions(message.channel, message.mentions[0], unmuted_perms)
                            await bot.send_message(message.channel, message.mentions[0].mention + " was unmuted in " + message.channel.mention + " by " + message.author.mention + ".")
                        elif len(message.mentions) < 1:
                            await bot.send_message(message.channel, mention + " You must mention the user you want to unmute on this channel.")
                        elif len(message.mentions) > 1:
                            await bot.send_message(message.channel, mention + " You may not unmute more than one member at a time.")
                    except discord.errors.Forbidden:
                        await bot.send_message(message.channel, mention + " lmao-bot eithers lacks the permission to unmute members or the member you tried to unmute is of an equal or higher role than lmao-bot. Make sure `Manage Channels` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to unmute.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to unmute members.")
                    return 'unmute'
            async def cmd_kick():
                if perms.manage_roles:
                    try:
                        if len(message.mentions) == 1:
                            if message.mentions[0] == bot.user:
                                await bot.send_message(message.channel, "Silly " + mention + ", I can't kick myself!")
                            elif message.mentions[0].id == "210220782012334081":
                                await bot.send_message(message.channel, "Please, " + mention + ", you can't kick my creator.")
                            else:
                                await bot.kick(message.mentions[0])
                                await bot.send_message(message.channel, "Goodbye, " + str(message.mentions[0]) + ", I'll see you in therapy!")
                        elif len(message.mentions) < 1:
                            await bot.send_message(message.channel, mention + " You must mention the user you want to kick from the server.")
                        elif len(message.mentions) > 1:
                            await bot.send_message(message.channel, mention + " You may not kick more than one member at a time.")
                    except discord.errors.Forbidden:
                        await bot.send_message(message.channel, mention + " lmao-bot eithers lacks the permission to kick members or the member you tried to kick is of an equal or higher role than lmao-bot. Make sure `Kick Members` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to kick.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to kick members.")
                return 'kick'
            async def cmd_ban():
                if perms.ban_members:
                    try:
                        if len(message.mentions) == 1:
                            if message.mentions[0] == bot.user:
                                await bot.send_message(message.channel, "Silly " + mention + ", I can't ban myself!")
                            elif message.mentions[0].id == "210220782012334081":
                                await bot.send_message(message.channel, "Please, " + mention + ", you can't ban my creator.")
                            else:
                                await bot.ban(message.mentions[0])
                                await bot.send_message(message.channel, "Goodbye, " + str(message.mentions[0]) + ", I'll see you in therapy! (Or never, 'cause, you know, you're banned...)")
                        elif len(message.mentions) < 1:
                            await bot.send_message(message.channel, mention + " You must mention the user you want to ban from the server.")
                        elif len(message.mentions) > 1:
                            await bot.send_message(message.channel, mention + " You may not ban more than one member at a time.")
                    except discord.errors.Forbidden:
                        await bot.send_message(message.channel, mention + " lmao-bot eithers lacks the permission to ban members or the member you tried to ban is of an equal or higher role than lmao-bot. Make sure `Ban Members` is enabled for lmao-bot and that lmao-bot is a higher role than the member you are trying to ban.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to ban members.")
                return 'ban'
            # Connects the bot to the voice channel the author is in; returns True if successful and False if not
            async def connect_voice():
                global voice
                if bot.is_voice_connected(server):
                    return True
                else:
                    if message.author.voice_channel != None:
                        voice[server_id] = await bot.join_voice_channel(message.author.voice_channel)
                        return True
                    else:
                        await bot.send_message(message.channel, mention + " You must be in a voice channel first.")
                        return False
            # Disconnects the bot from voice channels in the current server
            async def disconnect_voice():
                for vc in bot.voice_clients:
                    if vc.server == server:
                        await vc.disconnect()
                        break
            # Given a time in seconds, returns [h:mm:ss]
            def video_duration(time):
                t = lu.dhms_time(time)
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
            # Returns the video info in the form of Title [h:mm:ss], Title is not bold if bold=False
            def video_info(vid, bold=True):
                bold_mark = "**"
                if bold == False:
                    bold_mark = ""
                title = vid.title[:180]
                if title != vid.title:
                    title += "..."
                return bold_mark + title + bold_mark + " " + video_duration(vid.duration)
            # After a song finishes playing, the player will automatically start playing the next song in the queue
            def next_song():
                player[server_id][0].stop()
                player[server_id].pop(0)
                if len(player[server_id]) > 0:
                    reload_song = voice[server_id].create_ytdl_player(player[server_id][0].url, after=next_song)
                    song = asyncio.run_coroutine_threadsafe(reload_song, bot.loop)
                    try:
                        player[server_id][0] = song.result()
                        player[server_id][0].start()
                    except Exception as e:
                        template = str(datetime.now()) + "Playing next song failed. Exception: {0}. Arguments:\n{1!r}"
                        print(template.format(type(e).__name__, e.args))
                        #pass
                    coro_msg = bot.send_message(message.channel, ":arrow_forward: Now playing {}.".format(video_info(player[server_id][0])))
                else:
                    coro_dc = disconnect_voice()
                    dc = asyncio.run_coroutine_threadsafe(coro_dc, bot.loop)
                    try:
                        dc.result()
                    except Exception as e:
                        template = str(datetime.now()) + "Disconnecting voice failed. Exception: {0}. Arguments:\n{1!r}"
                        print(template.format(type(e).__name__, e.args))
                        #pass
                    coro_msg = bot.send_message(message.channel, ":stop_button: The queue has finished.")
                fut = asyncio.run_coroutine_threadsafe(coro_msg, bot.loop)
                try:
                    fut.result()
                except Exception as e:
                    template = str(datetime.now()) + "Message send failed. Exception: {0}. Arguments:\n{1!r}"
                    print(template.format(type(e).__name__, e.args))
                    #pass
            # Someone can add a new song to the queue, resume a paused song, or skip to a song later in the queue
            async def cmd_play():
                if not discord.opus.is_loaded():
                    discord.opus.load_opus('libopus.so')
                global player
                connected = await connect_voice()
                if connected:
                    await bot.send_typing(message.channel)
                    if cmd_arg == "":
                        await cmd_resume()
                        return 'play'
                    else:
                        skip = False
                        try:
                            i = int(cmd_arg) - 1
                            song_to_play = player[server_id][i]
                            player[server_id].insert(1, song_to_play)
                            player[server_id].pop(i + 1)
                            player[server_id].insert(2, player[server_id][0])
                            player[server_id][0].stop()
                            skip = True
                        except (IndexError, ValueError) as e:
                            try:
                                player[server_id].append(await voice[server_id].create_ytdl_player(cmd_arg, after=next_song))
                                await bot.send_message(message.channel, ":white_check_mark: Added {} to the queue.".format(video_info(player[server_id][len(player[server_id]) - 1])))
                            except Exception as ex:
                                template = str(datetime.now()) + "Not a URL. Exception: {0}. Arguments:\n{1!r}"
                                print(template.format(type(ex).__name__, ex.args))
                                try:
                                    player[server_id].append(await voice[server_id].create_ytdl_player("ytsearch:{" + cmd_arg + "}", after=next_song))
                                    await bot.send_message(message.channel, ":white_check_mark: Added {} to the queue.".format(video_info(player[server_id][len(player[server_id]) - 1])))
                                except Exception as exc:
                                    template = str(datetime.now()) + "No song found. Exception: {0}. Arguments:\n{1!r}"
                                    print(template.format(type(exc).__name__, exc.args))
                                    await bot.send_message(message.channel, ":x: " + mention + " No results were found on YouTube for **{}**. Try searching for the video's URL.".format(cmd_arg))
                                    return 'play'
                        if (len(player[server_id]) == 1):
                            await cmd_resume()
                        return 'play'
            # Skips to the next song in the queue
            async def cmd_next():
                global player
                connected = await connect_voice()
                if connected:
                    if len(player[server_id]) < 1:
                        await bot.send_message(message.channel, mention + " There are currently no songs in the queue.")
                    else:
                        player[server_id][0].stop()
                        if (len(player[server_id]) <= 0):
                            await disconnect_voice()
                            await bot.send_message(message.channel, ":stop_button: The queue has finished.")
                return 'next'
            # Pauses the current song in the queue
            async def cmd_pause():
                connected = await connect_voice()
                if connected:
                    if len(player[server_id]) > 0:
                        player[server_id][0].pause()
                        await bot.send_message(message.channel, ":pause_button: Paused {}. Use the `resume` command to resume.".format(video_info(player[server_id][0])))
                    else:
                        await bot.send_message(message.channel, "There is nothing in the queue to pause.")
                    return 'pause'
            # Resumes a paused song in the queue
            async def cmd_resume():
                global player
                global player_vol
                if len(player[server_id]) > 0:
                    try:
                        player[server_id][0].start()
                        player[server_id][0].pause()
                        player[server_id][0] = await voice[server_id].create_ytdl_player(player[server_id][0].url, after=next_song)
                        player[server_id][0].start()
                        #player[server_id][0].volume = player_vol[server_id]
                    except RuntimeError:
                        player[server_id][0].resume()
                    await bot.send_message(message.channel, ":arrow_forward: Now playing {}.".format(video_info(player[server_id][0])))
                else:
                    await bot.send_message(message.channel, mention + " There are currently no songs in the queue.")
                return 'resume'
            # Stops the queue
            async def cmd_stop():
                connected = await connect_voice()
                if connected:
                    if len(player[server_id]) > 0:
                        player[server_id][0].stop()
                        player[server_id] = []
                        await bot.send_message(message.channel, ":stop_button: The queue has been stopped.")
                        await disconnect_voice()
                    else:
                        await bot.send_message(message.channel, mention + " There are currently no songs in the queue.")
                        await disconnect_voice()
                return 'stop'
            # Lists the song in the queue and allows for people to add songs, remove songs, or clear the queue
            async def cmd_queue():
                global player
                q_cmd = cmd_arg.lower()
                q_arg = ""
                if cmd_arg.find(' ') != -1:
                    q_cmd = cmd_arg[:cmd_arg.find(' ')].lower()
                    q_arg = cmd_arg[cmd_arg.find(' ') + 1:]
                if q_cmd == "add":
                    connected = await connect_voice()
                    if connected:
                        await bot.send_typing(message.channel)
                        try:
                            player[server_id].append(await voice[server_id].create_ytdl_player(q_arg, after=next_song))
                            await bot.send_message(message.channel, ":white_check_mark: Added {} to the queue.".format(video_info(player[server_id][len(player[server_id]) - 1])))
                        except Exception as e:
                            template = str(datetime.now()) + "Not a URL. Exception: {0}. Arguments:\n{1!r}"
                            print(template.format(type(e).__name__, e.args))
                            try:
                                player[server_id].append(await voice[server_id].create_ytdl_player("ytsearch:{" + q_arg + "}", after=next_song))
                                await bot.send_message(message.channel, ":white_check_mark: Added {} to the queue.".format(video_info(player[server_id][len(player[server_id]) - 1])))
                            except Exception as ex:
                                template = str(datetime.now()) + "No song found. Exception: {0}. Arguments:\n{1!r}"
                                print(template.format(type(ex).__name__, ex.args))
                                await bot.send_message(message.channel, ":x: " + mention + " No results were found on YouTube for **{}**. Try searching for the video's URL.".format(q_arg))
                    return 'queue_add'
                elif q_cmd == "remove":
                    connected = await connect_voice()
                    if connected:
                        try:
                            i = int(q_arg) - 1
                            if (i <= 0):
                                await cmd_next()
                            else:
                                await bot.send_message(message.channel, ":wastebasket: {} has been removed from the queue.".format(video_info(player[server_id][i])))
                                player[server_id].pop(i)
                        except ValueError:
                            await bot.send_message(message.channel, mention + " You must include the number of the song in the queue you want to remove. e.g. `" + prefix + " q remove 3`")
                        except IndexError:
                            await bot.send_message(message.channel, mention + " Song #{} does not exist in the queue.".format(i))
                    return 'queue_remove'
                elif q_cmd == "clear":
                    connected = await connect_voice()
                    if connected:
                        while(len(player[server_id]) > 1):
                            player[server_id].pop(1)
                    await bot.send_message(message.channel, "The queue has been cleared.")
                    return 'queue_clear'
                else:
                    queue = []
                    if (len(player[server_id]) == 0):
                        await bot.send_message(message.channel, "No songs are currently in queue.")
                        return 'queue'
                    playtime = 0
                    for i in range(len(player[server_id])):
                        queue.append("{}. {}\n".format(i + 1, video_info(player[server_id][i], bold=False)))
                        playtime += player[server_id][i].duration
                    playtime_str = video_duration(playtime)
                    queue_msg = "**SONGS CURRENTLY IN QUEUE** {}:\n\n".format(playtime_str)
                    while(True):
                        if len(queue) == 0:
                            break
                        for i in range(10):
                            if len(queue) == 0:
                                break
                            queue_msg += queue[0]
                            queue.pop(0)
                        await bot.send_message(message.channel, queue_msg)
                        queue_msg = ""
                    return 'queue'
            async def cmd_booty():  # Sends a random SFW booty pic in the channel
                await bot.send_file(message.channel, 'img/booties/booty' + str(random.randint(1,10)) + '.jpg')
                return 'booty'
            async def cmd_moon():   # Allows users to moon other users with SFW booty pics
                mentioned = ""
                for mentioned_user in message.raw_mentions:
                    mentioned += "<@" + mentioned_user + "> "
                if mentioned != "":
                    mentioned = mentioned[:-1]
                    mention_msg = mentioned + ", you have been mooned by " + mention + "!"
                else:
                    mention_msg = ""
                await bot.send_file(message.channel, 'img/booties/booty' + str(random.randint(1,10)) + '.jpg', content=mention_msg)
                return 'moon'
            async def cmd_beautiful():
                await bot.send_typing(message.channel)
                try:
                    beautiful_person = message.mentions[0]
                except IndexError:
                    beautiful_person = message.author
                beautiful = await avatar.beautiful(beautiful_person)
                img_file = "img/beautiful_{}.png".format(beautiful_person.id)
                await bot.send_file(message.channel, img_file, content=beautiful_person.mention + " :heart:")
                os.remove(img_file)
                return 'beautiful'
            async def cmd_ugly():
                await bot.send_typing(message.channel)
                try:
                    ugly_person = message.mentions[0]
                except IndexError:
                    ugly_person = message.author
                ugly = await avatar.ugly(ugly_person)
                img_file = "img/ugly_{}.png".format(ugly_person.id)
                await bot.send_file(message.channel, img_file, content=ugly_person.mention + " :japanese_goblin:")
                os.remove(img_file)
                return 'ugly'
            async def cmd_triggered():
                await bot.send_typing(message.channel)
                try:
                    triggered_person = message.mentions[0]
                except IndexError:
                    triggered_person = message.author
                triggered = await avatar.triggered(triggered_person)
                img_file = "img/triggered_{}.png".format(triggered_person.id)
                await bot.send_file(message.channel, img_file, content=triggered_person.mention + " needs a safe space!")
                os.remove(img_file)
                return 'triggered'
            async def cmd_victory():
                await bot.send_typing(message.channel)
                try:
                    victory_person = message.mentions[0]
                except IndexError:
                    victory_person = message.author
                victory = await avatar.victory(victory_person)
                img_file = "img/victory_{}.png".format(victory_person.id)
                await bot.send_file(message.channel, "img/victory_{}.png".format(victory_person.id), content=victory_person.mention + " :trophy: Victory Royale!")
                os.remove(img_file)
                return 'victory'
            async def cmd_wanted():
                await bot.send_typing(message.channel)
                try:
                    wanted_person = message.mentions[0]
                except IndexError:
                    wanted_person = message.author
                wanted = await avatar.wanted(wanted_person)
                img_file = "img/wanted_{}.png".format(wanted_person.id)
                await bot.send_file(message.channel, img_file, content=wanted_person.mention + " is WANTED!")
                os.remove(img_file)
                return 'wanted'
            async def cmd_whos_that():
                await bot.send_typing(message.channel)
                try:
                    whos_that_person = message.mentions[0]
                except IndexError:
                    whos_that_person = message.author
                whos_that = await avatar.whos_that(whos_that_person)
                img_file = "img/whos_that_{}.png".format(whos_that_person.id)
                await bot.send_file(message.channel, img_file, content="Who's that Pokémon?\n\nIt's... " + whos_that_person.mention + "!")
                os.remove(img_file)
                return 'whos_that'
            async def cmd_seen_from_above():
                await bot.send_typing(message.channel)
                try:
                    seen_from_above_person = message.mentions[0]
                except IndexError:
                    seen_from_above_person = message.author
                seen_from_above = await avatar.seen_from_above(seen_from_above_person)
                img_file = "img/seen_from_above_{}.png".format(seen_from_above_person.id)
                await bot.send_file(message.channel, img_file, content="It's... " + seen_from_above_person.mention + ", seen from above!")
                os.remove(img_file)
                return 'seen_from_above'
            async def cmd_urban():
                await bot.send_typing(message.channel)
                #try:
                #    urban_def = urban.define(cmd_arg)[0]
                #    urban_msg = "**Urban Dictionary definition for {}:**\n\n{}\n\n\n**Example:**\n\n_{}_\n\n\n:thumbsup: {}     :thumbsdown: {}".format(urban_def.word, urban_def.definition, urban_def.example, urban_def.upvotes, urban_def.downvotes)
                #    await bot.send_message(message.channel, urban_msg)
                #except IndexError:
                #    await bot.send_message(message.channel, "Sorry, {} could not be found on Urban Dictionary.".format(cmd_arg))
                await bot.send_message(message.channel, "Sorry, this command is not available yet. Discord Bot List is strict about having this command being NSFW-channels-only, but my current library doesn't support that. Please be patient while the program is rewritten. :)")
                return 'urban'
            async def cmd_lmgtfy():
                await bot.send_typing(message.channel)
                await bot.send_message(message.channel, lmgtfy.lmgtfy(cmd_arg))
                return 'lmgtfy'
            async def cmd_coin():
                try:
                    if int(cmd_arg) > 100:
                        await bot.send_message(message.channel, "You may only flip up to 100 coins at a time.")
                        return 'coin'
                    elif int(cmd_arg) > 0:
                        coin_number = int(cmd_arg)
                    else:
                        coin_number = 1
                except ValueError:
                    coin_number = 1
                if coin_number == 1:
                    coin = random.randint(0,1)
                    gender = random.randint(0,1)
                    flip = "Heads! :man:"
                    if coin == 0:
                        flip = "Tails! :peach:"
                    elif gender == 0:
                        flip = "Heads! :woman:"
                    await bot.send_message(message.channel, mention + " " + flip)
                    return 'coin'
                coin_msg = mention + " You just flipped **" + str(coin_number) + "** coins and got **"
                coin_emoji = ""
                count = [0, 0]
                for flip_x in range(coin_number):
                    coin = random.randint(0,1)
                    gender = random.randint(0,1)
                    if coin == 1:
                        coin_msg += "T"
                        coin_emoji += " :peach:"
                    elif gender == 0:
                        coin_msg += "H"
                        coin_emoji += " :man:"
                    else:
                        coin_msg += "H"
                        coin_emoji += " :woman:"
                    count[coin] += 1
                coin_msg += "**!"
                coin_results = "\n`Heads: " + str(count[0]) + "`\n`Tails: " + str(count[1]) + "`"
                await bot.send_message(message.channel, coin_msg + coin_emoji + coin_results)
                return 'coin'
            async def cmd_dice():
                emoji = ["one",
                         "two",
                         "three",
                         "four",
                         "five",
                         "six"]
                try:
                    if int(cmd_arg) > 100:
                        await bot.send_message(message.channel, "You may only roll up to 100 dice at a time.")
                        return 'dice'
                    elif int(cmd_arg) > 0:
                        dice_number = int(cmd_arg)
                    else:
                        dice_number = 1
                except ValueError:
                    dice_number = 1
                dice_msg = mention + " :game_die: You just rolled a "
                dice_emoji = ""
                total = 0
                for roll_x in range(dice_number):
                    die = random.randint(1,6)
                    dice_msg += "**" + str(die) + "** + "
                    dice_emoji += ":" + emoji[die-1] + ":"
                    total += die
                dice_msg = dice_msg[:-3] + "! "
                await bot.send_message(message.channel, dice_msg + dice_emoji)
                if dice_number > 1:
                    dice_stats = "`Total:   " + str(total) + "`\n`Average: " + str(total / dice_number) + "`"
                    await bot.send_message(message.channel, dice_stats)
                return 'dice'
            async def cmd_card():
                global ranks
                global suits
                try:
                    if int(cmd_arg) > 52:
                        await bot.send_message(message.channel, "You may draw up to 52 cards.")
                        return 'card'
                    elif int(cmd_arg) > 0:
                        card_number = int(cmd_arg)
                    else:
                        card_number = 1
                except ValueError:
                    card_number = 1
                card_msg = mention + " :black_joker: You just drew "
                drawn = []
                rank = random.randint(1,13)
                suit = random.randint(1,4)
                for card_x in range(card_number):
                    while [rank, suit] in drawn:
                        rank = random.randint(1,13)
                        suit = random.randint(1,4)
                    card_msg += ranks[rank - 1] + suits[suit - 1] + " + "
                    drawn.append([rank, suit])
                card_msg = card_msg[:-3] + "! "
                await bot.send_message(message.channel, card_msg)
                return 'card'
            async def cmd_deal():
                global deck
                deck_msg = mention + " The full deck: "
                for card in deck[server_id]:
                    deck_msg += card[0] + card[1] + " "
                await bot.send_message(message.channel, deck_msg)
                return 'deal'
            async def cmd_8ball():
                responses = ["It is certain.",
                             "It is decidedly so.",
                             "Without a doubt.",
                             "Yes - definitely.",
                             "You may rely on it.",
                             "As I see it, yes.",
                             "Most likely.",
                             "Outlook good.",
                             "Yes.",
                             "Signs point to yes.",
                             "Reply hazy, try again.",
                             "Ask again later.",
                             "Better not tell you now.",
                             "Cannot predict now.",
                             "Concentrate and ask again.",
                             "Don't count on it.",
                             "My reply is no.",
                             "My sources say no.",
                             "Outlook not so good.",
                             "Very doubtful."]
                roll = random.randint(0,19)
                emoji = ":negative_squared_cross_mark:"
                if roll < 10:
                    emoji = ":white_check_mark:"
                elif roll < 15:
                    emoji = ":question:"
                await bot.send_message(message.channel, emoji + " " + mention + " " + responses[roll])
                return '8ball'
            async def cmd_pick():
                options = []
                #n = find(cmd_arg, ",")
                options_str = cmd_arg
                while options_str.find(",") != -1:
                    options.append((options_str[:options_str.find(",")]).strip())
                    options_str = options_str[options_str.find(",")+1:]
                options.append(options_str.strip())
                pick_msg = ["I'm in the mood for ",
                            "",
                            "Eeny, meeny, miny, moe. I pick ",
                            "Y'all get any more of those ",
                            "An obvious choice: ",
                            "Do you even need to ask? The obvious answer is "]
                after_msg = [" today.",
                             ", I choose you!",
                             ".",
                             "?",
                             ", naturally.",
                             "."]
                x = random.randint(0, len(pick_msg) - 1)
                y = random.randint(0, len(options) - 1)
                await bot.send_message(message.channel, mention + " " + pick_msg[x] + options[y] + after_msg[x])
                return 'pick'
            async def cmd_guess():
                global magic_number
                global guess_count
                if cmd_arg == "":
                    await replace_ass()
                elif magic_number[server_id] == -1:
                    if cmd_arg == "start":
                        magic_number[server_id] = random.randint(0,100)
                        print(str(datetime.now()) + " " + "Magic number for " + server.name + ": " + magic_number[server_id])
                        await bot.send_message(message.channel, "I'm thinking of a number from 0 to 100. Can you guess what it is? :thinking:")
                    else:
                        try:
                            number_guess = int(cmd_arg)
                            await bot.send_message(message.channel, "A guessing game is currently not in progress. To start one, say `" + prefix + " guess start`.")
                        except ValueError:
                            if cmd_arg == "giveup":
                                await bot.send_message(message.channel, "A guessing game is currently not in progress. To start one, say `" + prefix + " guess start`.")
                            else:
                                await replace_ass()
                else:
                    try:
                        number_guess = int(cmd_arg)
                        if number_guess == magic_number[server_id]:
                            await bot.send_message(message.channel, "Congratulations! " + str(number_guess) + " is correct!")
                            guess_count[server_id] += 1
                            magic_number[server_id] = -1
                            await bot.send_message(message.channel, "It took you " + str(guess_count[server_id]) + " guesses to guess my number.")
                            guess_count[server_id] = 0
                        elif number_guess < magic_number[server_id]:
                            await bot.send_message(message.channel, str(number_guess) + " is too low!")
                            guess_count[server_id] += 1
                        elif number_guess > magic_number[server_id]:
                            await bot.send_message(message.channel, str(number_guess) + " is too high!")
                            guess_count[server_id] += 1
                        else:
                            await bot.send_message(message.channel, 'Your guess must be an integer from 0 to 100!')
                    except ValueError:
                        if cmd_arg == "giveup":
                            await bot.send_message(message.channel, 'After ' + str(guess_count[server_id]) + r' guesses, you have already given up (_psst_ my number was ' + str(magic_number[server_id]) + r"). What's the point in playing if you're not even going to try?")
                            magic_number[server_id] = -1
                            guess_count[server_id] = 0
                        elif cmd_arg == "start":
                            await bot.send_message(message.channel, 'A game is already in progress!')
                        else:
                            await replace_ass()
                return 'guess'

            async def cmd_add():   #adds custom command
                if lmao_admin or perms.manage_messages:
                    custom_cmd = cmd_arg
                    space_ind = custom_cmd.find(' ')
                    if (space_ind == -1):
                        await bot.send_message(message.channel, mention + " You must include the following components to the command: `" + prefix + " add` `command_name` `command_text`")
                    else:
                        custom_cmd_name = custom_cmd[:space_ind]
                        custom_cmd_text = custom_cmd[space_ind + 1:]
                        if custom_cmd_name in custom_cmd_list[server_id]:
                            await bot.send_message(message.channel, mention + " " + custom_cmd_name + " already exists as a command.")
                        else:
                            custom_cmd_list[server_id][custom_cmd_name] = custom_cmd_text
                            await bot.send_message(message.channel, custom_cmd_name + " added as a custom command.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to add custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                return 'add'
            async def cmd_edit():  #edits existing custom command
                if lmao_admin or perms.manage_messages:
                    custom_cmd = cmd_arg
                    space_ind = custom_cmd.find(' ')
                    if (space_ind == -1):
                        await bot.send_message(message.channel, mention + " You must include the following components to the command: `" + prefix + " edit` `command_name` `new_command_text`")
                    else:
                        custom_cmd_name = custom_cmd[:space_ind]
                        custom_cmd_text = custom_cmd[space_ind + 1:]
                        if custom_cmd_name in custom_cmd_list[server_id]:
                            custom_cmd_list[server_id][custom_cmd_name] = custom_cmd_text
                            await bot.send_message(message.channel, custom_cmd_name + " custom command updated.")
                        else:
                            await bot.send_message(message.channel, custom_cmd_name + " does not exist as a command.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to edit custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                return 'edit'
            async def cmd_delete():    #deletes existing custom command
                if lmao_admin or perms.manage_messages:
                    custom_cmd = cmd_arg
                    if custom_cmd in custom_cmd_list[server_id]:
                        deleted_cmd_text = custom_cmd_list[server_id][custom_cmd]
                        del custom_cmd_list[server_id][custom_cmd]
                        await bot.send_message(message.channel, custom_cmd + " custom command deleted. It originally printed:")
                        await bot.send_message(message.channel, deleted_cmd_text)
                    else:
                        await bot.send_message(message.channel, custom_cmd + " does not exist as a command.")
                else:
                    await bot.send_message(message.channel, mention + " You do not have the permission to delete custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                return 'delete'
            async def cmd_list():  # lists all custom commands
                custom_cmd_list_msg = "**FULL LIST OF CUSTOM COMMANDS:**\n"
                for custom_cmd_key in custom_cmd_list[server_id].keys():
                    custom_cmd_list_msg += "\n`" + custom_cmd_key + "`\n" + custom_cmd_list[server_id][custom_cmd_key] + "\n"
                for i in range(0, len(custom_cmd_list_msg), 2000):
                    await bot.send_message(message.channel, custom_cmd_list_msg[i:i+2000])
                return 'list'
            async def cmd_custom():    # triggers custom command
                if msg.startswith(prefix.lower()):
                    try:
                        await bot.send_message(message.channel, custom_cmd_list[server_id][cmd_raw.strip()])
                        return 'custom'
                    except KeyError:
                        if "lmao" in msg or "lmfao" in msg:
                            await replace_ass()
                            return 'replace_ass'
                else:
                    if "lmao" in msg or "lmfao" in msg:
                        await replace_ass()
                        return 'replace_ass'

            cmd_case = {    # Dictionary for commmands
                "announce": cmd_announce,
                "changemaintenance": cmd_change_maintenance,
                "changegame": cmd_change_game,
                "help": cmd_help,
                "uptime": cmd_uptime,
                "ping": cmd_ping,
                "prefix": cmd_prefix,
                "about": cmd_about,
                "support": cmd_support,
                "invite": cmd_invite,
                "vote": cmd_vote,
                "say": cmd_say,
                "adminlist": cmd_admin_list,
                "addadmin": cmd_add_admin,
                "removeadmin": cmd_remove_admin,
                "purge": cmd_purge,
                "mute": cmd_mute,
                "unmute": cmd_unmute,
                "kick": cmd_kick,
                "ban": cmd_ban,
                "play": cmd_play,
                "next": cmd_next,
                "skip": cmd_next,
                "pause": cmd_pause,
                "resume": cmd_resume,
                "stop": cmd_stop,
                "queue": cmd_queue,
                "q": cmd_queue,
                "booty": cmd_booty,
                "moon": cmd_moon,
                "beautiful": cmd_beautiful,
                "ugly": cmd_ugly,
                "triggered": cmd_triggered,
                "victory": cmd_victory,
                "wanted": cmd_wanted,
                "whosthat": cmd_whos_that,
                "seenfromabove": cmd_seen_from_above,
                "urban": cmd_urban,
                "lmgtfy": cmd_lmgtfy,
                "toggleass": cmd_toggle_ass,
                "asstoggle": cmd_toggle_ass,
                "react": cmd_react,
                "togglereact": cmd_react,
                "reacttoggle": cmd_react,
                "on": cmd_toggle_ass,
                "off": cmd_toggle_ass,
                "lotto": cmd_toggle_ass,
                "chance": cmd_chance,
                "count": cmd_count,
                "coin": cmd_coin,
                "flip": cmd_coin,
                "dice": cmd_dice,
                "roll": cmd_dice,
                "card": cmd_card,
                "draw": cmd_card,
                "deal": cmd_deal,
                "8ball": cmd_8ball,
                "pick": cmd_pick,
                "guess": cmd_guess,
                "add": cmd_add,
                "edit": cmd_edit,
                "delete": cmd_delete,
                "list": cmd_list,
                "custom": cmd_custom
            }
            cmd_call = cmd_case.get(cmd_word, cmd_case.get('custom'))
            command_used = await cmd_call()
            if (command_used != None):
                update_usage(command_used)
                global last_use_time
                last_use_time = time.time()
        await cmd_switch(cmd_word)
        export_admins()
        await export_customs()

    elif msg == "lmao help":
        await bot.send_message(message.channel, "Type `" + prefix + " help` to see the help menu.")
    elif msg == "lmao prefix":
        await bot.send_message(message.channel, "My command prefix is currently `" + prefix + "`.")

    # GENERIC REPLY
    elif ('lmao' in msg or 'lmfao' in msg): #generic ass substitution
        update_usage("replace_ass")
        await replace_ass()

    if server_id == "345655060740440064" and ('pollard' in msg or 'buh-bye' in msg or 'buhbye' in msg or 'buh bye' in msg):
        x = random.randint(0,100)
        #if x <= react_chance[server_id]:
        emoji_list = bot.get_all_emojis()
        for emote in emoji_list:
            if emote.name == 'buhbye':
                emoji = emote
        try:
            await bot.add_reaction(message, emoji)
        except UnboundLocalError:
            pass
        except discord.errors.Forbidden:
            pass

    def export_settings():
        with io.open("settings.json") as f:
            settings_data = json.load(f)
            settings_data[server_id] = {
                "cmd_prefix": cmd_prefix[server_id],
                "replace_ass_chance": replace_ass_chance[server_id],
                "react_chance": react_chance[server_id]
            }
            new_settings_data = json.dumps(settings_data, indent=4)
            with io.open("settings.json", "w+", encoding="utf-8") as fo:
                fo.write(new_settings_data)
    export_settings()

bot.run(bot_token)
