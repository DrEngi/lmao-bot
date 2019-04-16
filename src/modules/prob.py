###PREFIX IS UNDEFINED
###ALLOW NO ARG - if not arg: #stuff

import discord
from discord.ext import commands
import random
from datetime import datetime
from utils import lbvars, usage

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

class Prob(commands.Cog):

    slots = ('bot', 'magic_number', 'guess_count')

    def __init__(self, bot):
        self.bot = bot
        self.magic_number = {}
        self.guess_count = {}

    @commands.command(name="coin", aliases=["flip"])
    async def cmd_coin(self, ctx, *, arg=""):
        try:
            if int(arg) > 100:
                await ctx.send("You may only flip up to 100 coins at a time.")
                return 'coin'
            elif int(arg) > 0:
                coin_number = int(arg)
            else:
                coin_number = 1
        except ValueError as e:
            coin_number = 1
        if coin_number == 1:
            coin = random.randint(0,1)
            gender = random.randint(0,1)
            flip = "Heads! :man:"
            if coin == 0:
                flip = "Tails! :peach:"
            elif gender == 0:
                flip = "Heads! :woman:"
            await ctx.send(ctx.author.mention + " " + flip)
            return 'coin'
        coin_msg = ctx.author.mention + " You just flipped **" + str(coin_number) + "** coins and got **"
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
        await ctx.send(coin_msg + coin_emoji + coin_results)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="dice", aliases=["roll"])
    async def cmd_dice(self, ctx, *, arg=""):
        emoji = ["one",
                 "two",
                 "three",
                 "four",
                 "five",
                 "six"]
        try:
            if int(arg) > 100:
                await ctx.send("You may only roll up to 100 dice at a time.")
                return 'dice'
            elif int(arg) > 0:
                dice_number = int(arg)
            else:
                dice_number = 1
        except ValueError:
            dice_number = 1
        dice_msg = ctx.author.mention + " :game_die: You just rolled a "
        dice_emoji = ""
        total = 0
        for roll_x in range(dice_number):
            die = random.randint(1,6)
            dice_msg += "**" + str(die) + "** + "
            dice_emoji += ":" + emoji[die-1] + ":"
            total += die
        dice_msg = dice_msg[:-3] + "! "
        await ctx.send(dice_msg + dice_emoji)
        if dice_number > 1:
            dice_stats = "`Total:   " + str(total) + "`\n`Average: " + str(total / dice_number) + "`"
            await ctx.send(dice_stats)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="card", aliases=["draw"])
    async def cmd_card(self, ctx, *, arg=""):
        try:
            if int(arg) > 52:
                await ctx.send("You may only draw up to 52 cards.")
                return 'card'
            elif int(arg) > 0:
                card_number = int(arg)
            else:
                card_number = 1
        except ValueError:
            card_number = 1
        card_msg = ctx.author.mention + " :black_joker: You just drew "
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
        await ctx.send(card_msg)
        usage.update(ctx)
        return ctx.command.name
    '''
    //Commented out because something appears to be broken here, at least there are a bunch of syntax errors.
    @commands.command(name="dice", aliases=["roll"])
    async def cmd_deal(self, ctx, *, arg=""):
        #global deck
        deck_msg = ctx.author.mention + " The full deck: "
        for card in deck[ctx.guild.id]:
            deck_msg += card[0] + card[1] + " "
        await ctx.send(deck_msg)
        return 'deal'

    def shuffle_cards(self, ctx):
        #The dream of creating a deal command is not dead, but possibly implement this through lbvars
        self.deck[ctx.guild.id] = []
        for rank in ranks:
            for suit in suits:
                deck[ctx.guild.id].append([rank, suit])
        random.shuffle(deck[ctx.guild.id])
    '''

    @commands.command(name="8ball", aliases=["eightball", "8-ball"])
    async def cmd_8ball(self, ctx):
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
        await ctx.send(emoji + " " + ctx.author.mention + " " + responses[roll])
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="pick", aliases=["choose, select"])
    async def cmd_pick(self, ctx, *, arg=""):
        options = []
        options_str = arg
        while options_str.find(",") != -1:
            options.append((options_str[:options_str.find(",")]).strip())
            options_str = options_str[options_str.find(",") + 1:]
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
        await ctx.send(ctx.author.mention + " " + pick_msg[x] + options[y] + after_msg[x])
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="guess")
    async def cmd_guess(self, ctx, guess=""):
        if ctx.guild.id not in self.magic_number:
            self.magic_number[ctx.guild.id] = -1
        if ctx.guild.id not in self.guess_count:
            self.guess_count[ctx.guild.id] = 0
        if self.magic_number[ctx.guild.id] == -1:
            if guess == "start":
                self.magic_number[ctx.guild.id] = random.randint(0,100)
                print(str(datetime.now()) + " " + "Magic number for {}: {}".format(ctx.guild.name, self.magic_number[ctx.guild.id]))
                await ctx.send("I'm thinking of a number from 0 to 100. Can you guess what it is? :thinking:")
            else:
                try:
                    number_guess = int(guess)
                    await ctx.send(f"A guessing game is currently not in progress. To start one, say `{ctx.prefix}guess start`.")
                except ValueError:
                    if guess == "giveup":
                        await ctx.send(f"A guessing game is currently not in progress. To start one, say `{ctx.prefix}guess start`.")
                    else:
                        await self.bot.get_command("replaceass").invoke(ctx)
        else:
            try:
                number_guess = int(guess)
                if number_guess == self.magic_number[ctx.guild.id]:
                    await ctx.send("Congratulations! " + str(number_guess) + " is correct!")
                    self.guess_count[ctx.guild.id] += 1
                    self.magic_number[ctx.guild.id] = -1
                    await ctx.send("It took you " + str(self.guess_count[ctx.guild.id]) + " guesses to guess my number.")
                    self.guess_count[ctx.guild.id] = 0
                elif number_guess < self.magic_number[ctx.guild.id]:
                    await ctx.send(str(number_guess) + " is too low!")
                    self.guess_count[ctx.guild.id] += 1
                elif number_guess > self.magic_number[ctx.guild.id]:
                    await ctx.send(str(number_guess) + " is too high!")
                    self.guess_count[ctx.guild.id] += 1
                else:
                    await ctx.send('Your guess must be an integer from 0 to 100!')
            except ValueError:
                if guess == "giveup" or guess == "quit" or guess == "exit":
                    await ctx.send('After ' + str(self.guess_count[ctx.guild.id]) + r' guesses, you have already given up (_psst_ my number was ' + str(self.magic_number[ctx.guild.id]) + r"). What's the point in playing if you're not even going to try?")
                    self.magic_number[ctx.guild.id] = -1
                    self.guess_count[ctx.guild.id] = 0
                elif guess == "start":
                    await ctx.send('A game is already in progress!')
                else:
                    await self.bot.get_command("replaceass").invoke(ctx)
        usage.update(ctx, guess)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Prob(bot))
