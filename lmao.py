### TO-DO LIST ###
###REWRITE TO NEW DISCORD.PY LIBRARY
#Add join/welcome message
#Add FAQ: lmao admins, command prefix, pronounce
#Server mute command
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

#Support server command
#Implement server count

import discord
import asyncio
import random
import io
import time
import aiohttp
import json
import urban
import avatar
import lmgtfy
from PIL import Image#, ImageDraw, ImageFont
#import urbandictionary as ud

bot = discord.Client()

bot_token = ""
with io.open("tokens/lmao.txt", "r") as token:
    bot_token = (token.read())[:-1]
dbl_token = ""
with io.open("tokens/lmao-dbl.txt", "r") as token:
    dbl_token = (token.read())[:-1]
dbl_url = "https://discordbots.org/api/bots/459432854821142529/stats"
dbl_headers = {"Authorization" : dbl_token}

### GLOBAL VARIABLES ###
start_time = 0.0            # Start time for lmao uptime command
cmd_prefix = {}             # Prefix for lmao-bot commands; default is "lmao "
lmao_admin_list = {}
custom_cmd_list = {}        # Dictionary for storing custom commands.
count_lmao = {}             # Counts how many times someone said lmao or lmfao in chat
count_lmao_full = ""        # Imports text from the count lmao file
replace_ass_chance = {}     # Chance of ass replacement
react_chance = {}           # Chance of ass reaction
magic_number = {}           # Magic number in number guessing game
guess_count = {}            # Number of guesses in number guessing game
deck = {}
init = []                   # Servers where settings have been initialized
server_count = 0
dm_count = 0

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

### UTILITY FUNCTIONS ###
# Utility function for finding the next occurrence of little_string in big_string after the index of n
def find_next(big_string, little_string, n):
    substr = big_string[n + 1:]
    return (substr.find(little_string) + len(big_string) - len(substr))
# Utility function for finding the nth occurrence of little_string in big_string
#def find_nth(big_string, little_string, n):
#    substr = big_string
#    for x in range(n - 1):
#        ind = big_string.find(little_string)
#        if ind == -1:
#            return -1
#        else:
#            substr = big_string[ind + 1:]
#    return big_string.find(little_string)
# Utility function for determining if an object is an integer
#def is_int(s):
#    try:
#        int(s)
#        return True
#    except ValueError:
#        return False

@bot.event
async def on_ready():   # Prints ready message in terminal
    global start_time
    start_time = time.time()
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(game=discord.Game(name=r'lmao help | Maintenance: 10pm ET | Created by Firestar493#6963'))
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(dbl_url, data=payload, headers=dbl_url)

@bot.event
async def on_server_join(server):
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(dbl_url, data=payload, headers=dbl_url)

@bot.event
async def on_server_remove(server):
    payload = {"server_count"  : len(bot.servers)}
    async with aiohttp.ClientSession() as aioclient:
        await aioclient.post(dbl_url, data=payload, headers=dbl_url)

@bot.event
async def on_member_join(member):
    if member.server.id == "463758816270483476":
        channel = member.server.get_channel("469491274219782144")
        await bot.send_typing(channel)
        beautiful = await avatar.beautiful(member)
        await bot.send_file(channel, "img/beautiful_person.png", content="Welcome to {}, {}!".format(member.server.name, member.mention))

@bot.event
async def on_message(message):  # Event triggers when message is sent
    channel = str(message.channel)
    author = str(message.author)
    author_dm = "Direct Message with " + author[:-5]
    perms = message.author.permissions_in(message.channel)
    if channel == author_dm:
        print(author + " sent: " + message.content)
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

    global init
    if server_id not in init:
        global cmd_prefix
        global lmao_admin_list
        global custom_cmd_list
        global count_lmao
        global replace_ass_chance
        global react_chance
        global magic_number
        global guess_count
        global server_count
        global dm_count

        try:
            settings_txt_r = io.open("settings/setting_" + server_id + ".txt", "r", encoding="utf-8")
        except FileNotFoundError:
            f = io.open("settings/setting_" + server_id + ".txt", "x", encoding="utf-8")
            f.close()
            cmd_prefix[server_id] = "lmao "
            replace_ass_chance[server_id] = 100
            react_chance[server_id] = 100
        else:
            settings_txt_r.seek(0)
            while True:
                line = settings_txt_r.readline()
                if line == "":
                    break
                elif line.startswith("cmd_prefix"):
                    space_ind = line.find(" ")
                    cmd_prefix[server_id] = line[space_ind + 1:-1]
                elif line.startswith("replace_ass_chance"):
                    space_ind = line.find(" ")
                    replace_ass_chance[server_id] = int(line[space_ind + 1:])
                elif line.startswith("react_chance"):
                    space_ind = line.find(" ")
                    react_chance[server_id] = int(line[space_ind + 1:])
            if server_id not in cmd_prefix.keys():
                cmd_prefix[server_id] = "lmao "
            if server_id not in replace_ass_chance.keys():
                replace_ass_chance[server_id] = 100
            if server_id not in react_chance.keys():
                react_chance[server_id] = 100
            settings_txt_r.seek(0)
            settings_txt_r.close()

        lmao_admin_list[server_id] = []
        magic_number[server_id] = -1
        guess_count[server_id] = 0
        shuffle_cards()
        if message.server == None:
            dm_count += 1
            print("{} initialized lmao-bot. The DM count is now {}.".format(str(message.author), dm_count))
        else:
            server_count += 1
            print("{} initialized lmao-bot. The server count is now {}.".format(message.server.name, server_count))
        init.append(server_id)

    lmao_admin = perms.administrator or message.author.id in lmao_admin_list[server_id] or message.author.id == "210220782012334081"
    #CONTINUE WORKING HERE

    if message.author != bot.user:

        prefix = cmd_prefix[server_id]
        msg_raw = message.content
        msg = msg_raw.lower()
        cmd_raw = msg_raw[len(prefix):]
        cmd = cmd_raw.lower() # The command that lmao bot responds to when called
        mention = message.author.mention
        replace_ass_msg = mention + ' You appear to have misplaced your ass while laughing. Here is a replacement: :peach:'

        async def replace_ass():    # Sends the ass substitution message
            x = random.randint(1, 100)
            global react_chance
            if x <= react_chance[server_id]:
                await bot.add_reaction(message, '🍑')
            y = random.randint(1, 100)
            global replace_ass_chance
            if y <= replace_ass_chance[server_id]:
                tmp = await bot.send_message(message.channel, replace_ass_msg)

        #global count_lmao
        #async def init_count_lmao():
        #    count_lmao_txt_r = io.open("count_lmao.txt", "r", encoding="utf-8")
        #    while True:
        #        line = (count_lmao_txt_r.readline())
        #        if (line.find(' ') != -1):
        #            cutoff_ind = line.find(' ')
        #            user = line[:cutoff_ind]
        #            count = int(line[cutoff_ind + 1:])
        #            count_lmao[user] = count
        #        else:
        #            break
        #    count_lmao_txt_r.seek(0)
        #    count_lmao_txt_r.seek(0)
        #    global count_lmao_full
        #    count_lmao_full = count_lmao_txt_r.read()
        #    count_lmao_txt_r.close()
        #await init_count_lmao()

        global custom_cmd_list
        async def import_customs():
            for cust_cmd in list(custom_cmd_list):
                del custom_cmd_list[cust_cmd]
            try:
                custom_cmd_list_txt_r = io.open("customs/custom_" + server_id + ".txt", "r", encoding="utf-8")
            except FileNotFoundError:
                f = io.open("customs/custom_" + server_id + ".txt", "x", encoding="utf-8")
                f.close()
            else:
                custom_cmd_list_txt_r.seek(0)
                while True:
                    line = custom_cmd_list_txt_r.readline()
                    if line == "":
                        break
                    else:
                        space_ind = line.find(' ')
                        cmd_name = line[:space_ind]
                        cmd_msg = line[space_ind + 1:-1]
                        custom_cmd_list[cmd_name] = cmd_msg
                custom_cmd_list_txt_r.seek(0)
                custom_cmd_list_txt_r.close()
        async def export_customs():
            custom_txt = ""
            for custom_cmd_key in custom_cmd_list.keys():
                custom_txt += custom_cmd_key + " " + custom_cmd_list[custom_cmd_key] + u'\u000A'
            custom_cmd_list_txt_w = io.open("customs/custom_" + server_id + ".txt", "w+", encoding="utf-8")
            custom_cmd_list_txt_w.write(custom_txt)
            custom_cmd_list_txt_w.close()

        async def import_admins():
            try:
                lmao_admin_list_txt_r = io.open("admins/admin_" + server_id + ".txt", "r", encoding="utf-8")
            except FileNotFoundError:
                f = io.open("admins/admin_" + server_id + ".txt", "x", encoding="utf-8")
                f.close()
            else:
                lmao_admin_list_txt_r.seek(0)
                while True:
                    line = lmao_admin_list_txt_r.readline()
                    if line == "":
                        break
                    else:
                        if line[:-1] not in lmao_admin_list[server_id]:
                            lmao_admin_list[server_id].append(line[:-1])
                lmao_admin_list_txt_r.seek(0)
                lmao_admin_list_txt_r.close()
        async def export_admins():
            admin_txt = ""
            for admin in lmao_admin_list[server_id]:
                admin_txt += admin + u'\u000A'
            lmao_admin_list_txt_w = io.open("admins/admin_" + server_id + ".txt", "w", encoding="utf-8")
            lmao_admin_list_txt_w.write(admin_txt)
            lmao_admin_list_txt_w.close()

        # PRIMARY FUNCTIONS
        if msg.startswith(prefix.lower()): # Bot reacts to command prefix call
            space_ind = cmd.find(' ')
            cmd_word = cmd
            cmd_arg = ""
            if space_ind != -1:
                cmd_word = cmd[:space_ind]
                cmd_arg = cmd_raw[space_ind+1:]
            await import_admins()
            await import_customs()
            async def cmd_switch(command):
                async def cmd_announce():
                    if message.author.id == "210220782012334081":
                        server_list = bot.servers
                        for server in server_list:
                            await asyncio.sleep(10)
                            for channel in server.channels:
                                if channel.permissions_for(server.me).send_messages and str(channel.type) == "text":
                                    with io.open("announcement_finished.txt", "a") as f:
                                        f.write("{} ({}) has received your announcement.".format(server.name, server.id))
                                    await bot.send_message(channel, cmd_arg)
                                    break
                    else:
                        await replace_ass()
                    return 'announce'
                async def cmd_uptime():
                    global start_time
                    current_time = time.time()
                    time_display = ""
                    seconds = round(current_time - start_time)
                    minutes = int(seconds / 60)
                    seconds -= minutes * 60
                    hours = int(minutes / 60)
                    minutes -= hours * 60
                    days = int(hours / 24)
                    hours -= days * 24
                    if days > 0:
                        time_display += str(days) + " day(s), " + str(hours) + " hour(s), " + str(minutes) + " minute(s), and "
                    elif hours > 0:
                        time_display += str(hours) + " hour(s), " + str(minutes) + " minute(s), and "
                    elif minutes > 0:
                        time_display += str(minutes) + " minute(s) and "
                    time_display += str(seconds) + " second(s)."
                    with io.open("next_maintenance.txt") as f:
                        next_maintenance = f.read()[:-1]
                    tmp = await bot.send_message(message.channel, "lmao-bot has been up for {}\n\nNext maintenance break is scheduled for {}.".format(time_display, next_maintenance))
                    return 'uptime'
                async def cmd_toggle_ass(): # Toggle whether automatic ass substitution happens or not
                    #if toggle_ass:
                    #    tmp = await bot.send_message(message.channel, 'Automatic ass substitution has been enabled. Hold onto your buns.')
                    #else:
                    #    tmp = await bot.send_message(message.channel, 'Automatic ass substitution has been disabled. Don\'t do anything reckless.')
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
                            tmp = await bot.send_message(message.channel, r'You have changed the automatic ass replacement chance to ' + str(replace_ass_chance[server_id]) + r"%. " + after_msg)
                        else:
                            tmp = await bot.send_message(message.channel, r'You must include an integer after toggleass from 0 to 100. This is the chance (in %) of automatic ass replacement.')
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to change the ass replacement chance. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                    return 'toggle_ass'
                async def cmd_toggle_react():
                    #global toggle_react
                    #toggle_react[server_id] = not toggle_react[server_id]
                    #if toggle_react[server_id]:
                    #    tmp = await bot.send_message(message.channel, 'Reactions have been enabled. Watch out for the Fine Bros. :eyes:')
                    #else:
                    #    tmp = await bot.send_message(message.channel, 'Reactions have been disabled. Looks like the Fine Bros found us. :pensive:')
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
                            await bot.send_message(message.channel, r'You must include an integer after togglereact from 0 to 100. This is the chance (in %) of automatic emoji reactions.')
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to change the reaction chance. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                    return 'toggle_react'
                async def cmd_chance():
                    global replace_ass_chance
                    #after_replace = ""
                    #if replace_ass_chance[server_id] < 50:
                    #    after_replace = "Tread carefully, and hold onto your buns."
                    #else:
                    #    after_replace = "Don't do anything reckless; you'll be fine."
                    #tmp = await bot.send_message(message.channel, r'The chance that you will have an ass replacement after laughing your ass off is ' + str(replace_ass_chance[server_id]) + r'%. ' + after_replace)
                    global react_chance
                    #after_react = ""
                    #if react_chance[server_id] == 0:
                    #    after_react = "Looks like the Fine Bros found us. :pensive:"
                    #else:
                    #    after_react = "Watch out for the Fine Bros. :eyes:"
                    #tmp = await bot.send_message(message.channel, r'The chance that you will receive a :peach: reaction after laughing your ass off is ' + str(react_chance[server_id]) + r'%. ' + after_react)
                    await bot.send_message(message.channel, "Ass replacement chance: **" + str(replace_ass_chance[server_id]) + "%**\nAss reaction chance: **" + str(react_chance[server_id]) + "%**")
                    return 'chance'
                async def cmd_help():   # DMs list of commands
                    await bot.send_typing(message.channel)
                    dm_help = [""":peach: **FULL LIST OF LMAO-BOT COMMANDS** :peach:
                                  \n
                                  \n:robot: **Bot Management** :robot:
                                  \n:exclamation: `lmao prefix` If the bot's command prefix is not \"lmao \", this returns the current command prefix.
                                  \n:question: `{0}help` Returns a list of commands for lmao-bot to your DMs (hey, that's meta).
                                  \n:computer: `{0}uptime` Shows how long lmao-bot has been up for as well as the time for the next maintenance break.
                                  \n:ping_pong: `{0}ping` Returns \"pong\".
                                  \n:exclamation: `{0}prefix` `new_prefix` Changes the bot's command prefix to `new_prefix`. Available to server admins and lmao admins only. Default is "lmao ".
                                  \n:information_source: `{0}about` Gives a brief description about the bot, including an invite to the support server.
                                  \n:ballot_box: `{0}vote` Like lmao-bot? This gives you a link to vote for it on Discord Bot List!""",
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
                                  \n:gear: **Lmao Message & Reaction Settings** :gear:
                                  \n:peach: `{0}toggleass` `chance` Changes the chance of automatic ass replacement after someone laughs their ass off to `chance` percent. Default is 100%.
                                  \n:peach: `{0}asstoggle` `chance` Does the same thing as `{0}toggleass`.
                                  \n:thumbsup: `{0}on` Changes the chance of automatic ass replacement to 100%.
                                  \n:thumbsdown: `{0}off` Changes the chance of automatic ass replacement to 0%.
                                  \n:slot_machine: `{0}lotto` Changes the chance of automatic ass replacement to 1% (spicy setting for spicy servers).
                                  \n:astonished: `{0}togglereact` `chance` Changes the chance of emoji reaction features to `chance` percent. Default is 100%.
                                  \n:astonished: `{0}reacttoggle` `chance` Does the same thing as `{0}togglereact`.
                                  \n:chart_with_upwards_trend: `{0}chance` Returns the chance of automatic ass replacement and the chance of emoji reaction features.
                                  \n:100: `{0}count` Counts the number of times you have used \"lmao\" or \"lmfao\".""",
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
                        await bot.send_message(message.author, msg_part.format(prefix))
                        asyncio.sleep(0.5)
                    await bot.send_message(message.channel, mention + ' A full list of lmao-bot commands has been slid into your DMs. :mailbox_with_mail:')
                    return 'help'
                async def cmd_count():  # Counts the number of times someone says lmao
                    #if message.author.id in count_lmao.keys():
                    #    await bot.send_message(message.channel, mention + " You have laughed your ass off " + str(count_lmao[message.author.id]) + " times.")
                    #else:
                    #    await bot.send_message(message.channel, mention + " You have yet to laugh your ass off.")
                    await bot.send_message(message.channel, mention + " Sorry, the count command is currently bugged and not working. This is a problem that is being worked on. :)")
                    return 'count'
                async def cmd_ping():   # Ping-Pong
                    await bot.send_message(message.channel, ':ping_pong: Pong')
                    return 'ping'
                async def cmd_prefix():
                    global cmd_prefix
                    if lmao_admin:
                        if cmd_arg == "":
                            await bot.send_message(message.channel, "To update the command prefix, type `" + cmd_prefix[server_id] + "prefix \"new_prefix\"`.")
                        elif cmd_arg[0:1] != "\"" or cmd_arg[-1:len(cmd_arg)] != "\"":
                            await bot.send_message(message.channel, "You must surround your new prefix with quotation marks to change the prefix. e.g. `" + cmd_prefix[server_id] + "prefix \"new_prefix\"`.")
                        elif "\n" in cmd_arg:
                            await bot.send_message(message.channel, "Your command prefix may not contain line breaks.")
                        elif len(cmd_arg[1:-1]) > 20:
                            await bot.send_message(message.channel, "Your command prefix may not be longer than 20 characters.")
                        else:
                            cmd_prefix[server_id] = cmd_arg[1:-1]
                            await bot.send_message(message.channel, "The prefix for lmao-bot is now \"" + cmd_prefix[server_id] + "\".")
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to change the bot's prefix. Ask a server administrator or lmao administrator to do so.")
                    return 'prefix'
                async def cmd_about():  # Returns about lmao-bot message
                    await bot.send_message(message.channel, """**About lmao-bot**: lmao-bot was created by Firestar493#6963 in June 2018 as a fun Discord bot for replacing people's asses after they \"lmao\" or \"lmfao\". The bot is written in Python using the discord.py library, and the support server is https://discord.gg/JQgB7p7.
                        \n\nlmao-bot is currently replacing asses on **{}** servers.
                        \n\nLike lmao-bot? **Vote** for lmao-bot on Discord Bot List! https://discordbots.org/bot/459432854821142529/vote""".format(len(bot.servers)))
                    return 'about'
                async def cmd_vote():
                    await bot.send_message(message.channel, "Like lmao-bot? **Vote** for lmao-bot on Discord Bot List!\n\nhttps://discordbots.org/bot/459432854821142529/vote")
                    return 'vote'
                async def cmd_say():    # Allows user to have lmao-bot say a message
                    if cmd_arg == "":
                        tmp = await bot.send_message(message.channel, 'You have to have a message for me to say. e.g. `" + prefix + "say Replacing asses by day, kicking asses by night.`')
                    else:
                        try:
                            await bot.delete_message(message)
                        except discord.errors.Forbidden:
                            print('The original message could not be deleted due to insufficient permissions. Make sure "Manage Messages" is enabled for lmao-bot.')
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
                            await bot.send_message(message.channel, mention + " You must specify the number of messages to purge. e.g. `" + prefix + "purge 5`")
                        except discord.errors.Forbidden:
                            await bot.send_message(message.channel, mention + " The messages could not be purged due to insufficient permissions for lmao-bot. Make sure `Manage Messages` is enabled for lmao-bot.")
                        return 'purge'
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to manage messages.")
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
                    #msg.mentions returns a list of Members mentioned
                    return 'moon'
                async def cmd_beautiful():
                    await bot.send_typing(message.channel)
                    try:
                        beautiful_person = message.mentions[0]
                    except IndexError:
                        beautiful_person = message.author
                    beautiful = await avatar.beautiful(beautiful_person)
                    await bot.send_file(message.channel, "img/beautiful_person.png", content=beautiful_person.mention + " :heart:")
                    return 'beautiful'
                async def cmd_ugly():
                    await bot.send_typing(message.channel)
                    try:
                        ugly_person = message.mentions[0]
                    except IndexError:
                        ugly_person = message.author
                    ugly = await avatar.ugly(ugly_person)
                    await bot.send_file(message.channel, "img/ugly_person.png", content=ugly_person.mention + " :japanese_goblin:")
                    return 'ugly'
                async def cmd_triggered():
                    await bot.send_typing(message.channel)
                    try:
                        triggered_person = message.mentions[0]
                    except IndexError:
                        triggered_person = message.author
                    triggered = await avatar.triggered(triggered_person)
                    await bot.send_file(message.channel, "img/triggered_person.png", content=triggered_person.mention + " needs a safe space!")
                    return 'triggered'
                async def cmd_victory():
                    await bot.send_typing(message.channel)
                    try:
                        victory_person = message.mentions[0]
                    except IndexError:
                        victory_person = message.author
                    victory = await avatar.victory(victory_person)
                    await bot.send_file(message.channel, "img/victory_person.png", content=victory_person.mention + " :trophy: Victory Royale!")
                    return 'victory'
                async def cmd_wanted():
                    await bot.send_typing(message.channel)
                    try:
                        wanted_person = message.mentions[0]
                    except IndexError:
                        wanted_person = message.author
                    wanted = await avatar.wanted(wanted_person)
                    await bot.send_file(message.channel, "img/wanted_person.png", content=wanted_person.mention + " is WANTED!")
                    return 'wanted'
                async def cmd_whos_that():
                    await bot.send_typing(message.channel)
                    try:
                        whos_that_person = message.mentions[0]
                    except IndexError:
                        whos_that_person = message.author
                    whos_that = await avatar.whos_that(whos_that_person)
                    await bot.send_file(message.channel, "img/whos_that_person.png", content="Who's that Pokémon?\n\nIt's " + whos_that_person.mention + ", seen from above!")
                    return 'wanted'
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
                            tmp = await bot.send_message(message.channel, "You may only flip up to 100 coins at a time.")
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
                        tmp = await bot.send_message(message.channel, mention + " " + flip)
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
                    tmp = await bot.send_message(message.channel, coin_msg + coin_emoji + coin_results)
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
                            tmp = await bot.send_message(message.channel, "You may only roll up to 100 dice at a time.")
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
                    tmp = await bot.send_message(message.channel, dice_msg + dice_emoji)
                    if dice_number > 1:
                        dice_stats = "`Total:   " + str(total) + "`\n`Average: " + str(total / dice_number) + "`"
                        tmp = await bot.send_message(message.channel, dice_stats)
                    return 'dice'
                async def cmd_card():
                    global ranks
                    global suits
                    try:
                        if int(cmd_arg) > 52:
                            tmp = await bot.send_message(message.channel, "You may draw up to 52 cards.")
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
                    tmp = await bot.send_message(message.channel, card_msg)
                    return 'card'
                async def cmd_deal():
                    global deck
                    deck_msg = mention + " The full deck: "
                    for card in deck[server_id]:
                        deck_msg += card[0] + card[1] + " "
                    await bot.send_message(message.channel, deck_msg)
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
                    tmp = await bot.send_message(message.channel, emoji + " " + mention + " " + responses[roll])
                    return '8ball'
                async def cmd_pick():
                    options = []
                    cmd_arg = message.content[10:]
                    #n = find(cmd_arg, ",")
                    while cmd_arg.find(",") != -1:
                        options.append((cmd_arg[:cmd_arg.find(",")]).strip())
                        cmd_arg = cmd_arg[cmd_arg.find(",")+1:]
                    options.append(cmd_arg.strip())
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
                    tmp = await bot.send_message(message.channel, mention + " " + pick_msg[x] + options[y] + after_msg[x])
                async def cmd_guess():
                    global magic_number
                    global guess_count
                    if cmd_arg == "":
                        await replace_ass()
                    elif magic_number[server_id] == -1:
                        if cmd_arg == "start":
                            magic_number[server_id] = random.randint(0,100)
                            print(magic_number[server_id])
                            tmp = await bot.send_message(message.channel, "I'm thinking of a number from 0 to 100. Can you guess what it is? :thinking:")
                        else:
                            try:
                                number_guess = int(cmd_arg)
                                tmp = await bot.send_message(message.channel, "A guessing game is currently not in progress. To start one, say `" + prefix + "guess start`.")
                            except ValueError:
                                if cmd_arg == "giveup":
                                    tmp = await bot.send_message(message.channel, "A guessing game is currently not in progress. To start one, say `" + prefix + "guess start`.")
                                else:
                                    await replace_ass()
                    else:
                        try:
                            number_guess = int(cmd_arg)
                            if number_guess == magic_number[server_id]:
                                tmp = await bot.send_message(message.channel, "Congratulations! " + str(number_guess) + " is correct!")
                                guess_count[server_id] += 1
                                magic_number[server_id] = -1
                                tmp = await bot.send_message(message.channel, "It took you " + str(guess_count[server_id]) + " guesses to guess my number.")
                                guess_count[server_id] = 0
                            elif number_guess < magic_number[server_id]:
                                tmp = await bot.send_message(message.channel, str(number_guess) + " is too low!")
                                guess_count[server_id] += 1
                            elif number_guess > magic_number[server_id]:
                                tmp = await bot.send_message(message.channel, str(number_guess) + " is too high!")
                                guess_count[server_id] += 1
                            else:
                                tmp = await bot.send_message(message.channel, 'Your guess must be an integer from 0 to 100!')
                        except ValueError:
                            if cmd_arg == "giveup":
                                #tmp = await bot.send_message(message.channel, 'You have ended the game. What a buzzkill.')
                                tmp = await bot.send_message(message.channel, 'After ' + str(guess_count[server_id]) + r' guesses, you have already given up (_psst_ my number was ' + str(magic_number[server_id]) + r"). What's the point in playing if you're not even going to try?")
                                magic_number[server_id] = -1
                                guess_count[server_id] = 0
                            elif cmd_arg == "start":
                                tmp = await bot.send_message(message.channel, 'A game is already in progress!')
                            else:
                                await replace_ass()
                    return 'guess'

                async def cmd_add():   #adds custom command
                    if lmao_admin or perms.manage_messages:
                        custom_cmd = cmd_arg
                        space_ind = custom_cmd.find(' ')
                        if (space_ind == -1):
                            tmp = await bot.send_message(message.channel, mention + " You must include the following components to the command: `" + prefix + "add` `command_name` `command_text`")
                        else:
                            custom_cmd_name = custom_cmd[:space_ind]
                            custom_cmd_text = custom_cmd[space_ind + 1:]
                            if custom_cmd_name in custom_cmd_list:
                                tmp = await bot.send_message(message.channel, mention + " " + custom_cmd_name + " already exists as a command.")
                            elif "\n" in custom_cmd:
                                tmp = await bot.send_message(message.channel, mention + " Your command message may not contain line breaks (at least for now).")
                            else:
                                custom_cmd_list[custom_cmd_name] = custom_cmd_text
                                tmp = await bot.send_message(message.channel, custom_cmd_name + " added as a custom command.")
                            #custom_cmd_list[custom_cmd]
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to add custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                    return 'add'
                async def cmd_edit():  #edits existing custom command
                    if lmao_admin or perms.manage_messages:
                        custom_cmd = cmd_arg
                        space_ind = custom_cmd.find(' ')
                        if (space_ind == -1):
                            tmp = await bot.send_message(message.channel, mention + " You must include the following components to the command: `" + prefix + "edit` `command_name` `new_command_text`")
                        elif "\n" in custom_cmd:
                            tmp = await bot.send_message(message.channel, mention + " Your command message may not contain line breaks (at least for now).")
                        else:
                            custom_cmd_name = custom_cmd[:space_ind]
                            custom_cmd_text = custom_cmd[space_ind + 1:]
                            if custom_cmd_name in custom_cmd_list:
                                custom_cmd_list[custom_cmd_name] = custom_cmd_text
                                await bot.send_message(message.channel, custom_cmd_name + " custom command updated.")
                            else:
                                await bot.send_message(message.channel, custom_cmd_name + " does not exist as a command.")
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to edit custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                    return 'edit'
                async def cmd_delete():    #deletes existing custom command
                    if lmao_admin or perms.manage_messages:
                        custom_cmd = cmd_arg
                        if custom_cmd in custom_cmd_list:
                            deleted_cmd_text = custom_cmd_list[custom_cmd]
                            del custom_cmd_list[custom_cmd]
                            await bot.send_message(message.channel, custom_cmd + " custom command deleted. It originally printed:")
                            await bot.send_message(message.channel, deleted_cmd_text)
                        else:
                            await bot.send_message(message.channel, custom_cmd + " does not exist as a command.")
                    else:
                        await bot.send_message(message.channel, mention + " You do not have the permission to delete custom commands. Ask a server administrator, lmao administrator, or user with the `Manage Messages` permission to do so.")
                    return 'delete'
                async def cmd_list():  # lists all custom commands
                    custom_cmd_list_msg = "**Full list of custom commands:**\n"
                    #tmp = await bot.send_message(message.channel, "**Full list of custom commands:**")
                    for custom_cmd_key in custom_cmd_list.keys():
                        custom_cmd_list_msg += "\n**" + custom_cmd_key + ":** " + custom_cmd_list[custom_cmd_key]
                    for i in range(0, len(custom_cmd_list_msg), 2000):
                        await bot.send_message(message.channel, custom_cmd_list_msg[i:i+2000])
                    #tmp = await bot.send_message(message.channel, 'List is not yet available.')
                    return 'list'
                async def cmd_custom():    # triggers custom command
                    if msg.startswith(prefix.lower()):
                        try:
                            await bot.send_message(message.channel, custom_cmd_list[cmd_raw])
                        except KeyError:
                            if "lmao" in msg or "lmfao" in msg:
                                await replace_ass()
                    else:
                        if "lmao" in msg or "lmfao" in msg:
                            await replace_ass()
                    return 'custom'

                cmd_case = {    # Dictionary for commmands
                    "announce": cmd_announce,
                    "help": cmd_help,
                    "uptime": cmd_uptime,
                    "ping": cmd_ping,
                    "prefix": cmd_prefix,
                    "about": cmd_about,
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
                    "booty": cmd_booty,
                    "moon": cmd_moon,
                    "beautiful": cmd_beautiful,
                    "ugly": cmd_ugly,
                    "triggered": cmd_triggered,
                    "victory": cmd_victory,
                    "wanted": cmd_wanted,
                    #"whosthat": cmd_whos_that,
                    "urban": cmd_urban,
                    "lmgtfy": cmd_lmgtfy,
                    "toggleass": cmd_toggle_ass,
                    "asstoggle": cmd_toggle_ass,
                    "togglereact": cmd_toggle_react,
                    "reacttoggle": cmd_toggle_react,
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
                #cmd_msg = await cmd_case[cmd]()
                cmd_call = cmd_case.get(cmd_word, cmd_case.get('custom'))
                #cmd_call = cmd_case.get(cmd, lambda: cmd_msg('default'))
                #cmd_msg = await cmd_case[cmd_call]()
                #tmp = await bot.send_message(message.channel, await cmd_call())
                await cmd_call()
            await cmd_switch(cmd_word)
            await export_admins()
            await export_customs()

        elif msg == "lmao help":
            await bot.send_message(message.channel, "Type `" + prefix + "help` to see the help menu.")
        elif msg == "lmao prefix":
            await bot.send_message(message.channel, "My command prefix is currently \"" + prefix + "\".")

        # GENERIC REPLY
        elif ('lmao' in msg or 'lmfao' in msg): #generic ass substitution
            #if toggle_ass:
            #    await replace_ass()
            await replace_ass()
            #count_lmao_txt_w = io.open("count_lmao.txt", "w", encoding="utf-8")
            #global count_lmao_full
            #if message.author.id in count_lmao.keys():
            #    count_lmao[message.author.id] += 1
            #    line_ind = (count_lmao_full).find(message.author.id)
            #    global find_next
            #    line_end = find_next(count_lmao_full, "\n", line_ind)
            #    text_prior = (count_lmao_full)[:line_ind]
            #    text_after = (count_lmao_full)[line_end + 1:]
            #    count_lmao_txt_w.write(text_prior + text_after + message.author.id + ' ' + str(count_lmao[message.author.id]) + u'\u000A')
            #else:
            #    count_lmao[message.author.id] = 1
            #    count_lmao_txt_w.write(count_lmao_full + message.author.id + ' ' + u'\u000A')

            #count_lmao_txt_w.close()

        if server_id == "345655060740440064" and ('pollard' in msg or 'buh-bye' in msg or 'buhbye' in msg or 'buh bye' in msg):
            x = random.randint(0,100)
            if x <= react_chance[server_id]:
                emoji_list = bot.get_all_emojis()
                for emote in emoji_list:
                    if emote.name == 'buhbye':
                        emoji = emote
                try:
                    await bot.add_reaction(message, emoji)
                except UnboundLocalError:
                    print('Emoji not found.')

        async def export_settings():
            global replace_ass_chance
            global react_chance
            settings_txt_w = io.open("settings/setting_" + server_id + ".txt", "w+", encoding="utf-8")
            settings_txt_w.write("cmd_prefix " + cmd_prefix[server_id] + "\nreplace_ass_chance " + str(replace_ass_chance[server_id]) + "\nreact_chance " + str(react_chance[server_id]))
            #settings_txt_w.write("replace_ass_chance " + str(replace_ass_chance[server_id]) + "\nreact_chance " + str(react_chance[server_id]))
            settings_txt_w.close()
        await export_settings()

#with io.open("tokens/lmao.txt", "r") as token:
    #bot.run((token.read())[:-1])
bot.run(bot_token)
