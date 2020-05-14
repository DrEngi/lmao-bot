using Discord.Commands;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class ProbabilityModule : ModuleBase
    {
        [Command("coin")]
        [Alias("flip")]
        [Summary("Flip a coin!")]
        public async Task<RuntimeResult> CoinFlip(int coin = 1)
        {
            if (coin > 100) return CustomResult.FromError("You may only flip up to 100 coins at a time");
            else if (coin <= 0) coin = 1;

            if (coin == 1)
            {
                Random rnd = new Random();
                int result = rnd.Next(0, 1);
                int gender = rnd.Next(0, 1);
                string flip = "Heads! :man:";

                if (result == 0)
                {
                    flip = "Tails! :peach:";
                }
                else if (gender == 0)
                {
                    flip = "Heads! :woman";
                }
                await ReplyAsync(Context.User.Mention + " " + flip);
                return CustomResult.FromSuccess();
            }
            else
            {
                string coinMessage = Context.User.Mention + " You just flipped **" + coin + "** coins and got **";
                string coinEmoji = "";

                Random rnd = new Random();
                int heads = 0;
                int tails = 0;
                for (int i = 0; i < coin; i++)
                {
                    int result = rnd.Next(0, 2);
                    int gender = rnd.Next(0, 2);

                    if (result == 1)
                    {
                        coinMessage += "T";
                        coinEmoji += " :peach:";
                        tails++;
                    }
                    if (result == 0)
                    {
                        if (gender == 0)
                        {
                            coinMessage += "H";
                            coinEmoji += " :man:";
                        }
                        else if (gender == 1)
                        {
                            coinMessage += "H";
                            coinEmoji += ":woman:";
                        }
                        heads++;
                    }
                }
                coinMessage += "**!";
                string coin_results = "\n`Heads: " + heads + "`\n`Tails: " + tails + "`";
                await ReplyAsync(coinMessage + coinEmoji + coin_results);
                return CustomResult.FromSuccess();
            }
        }

        [Command("dice")]
        [Alias("roll")]
        [Summary("Roll the dice!")]
        public async Task<RuntimeResult> RollDice(int dice = 1)
        {
            List<string> emojis = new List<string>()
            {
                "one",
                "two",
                "three",
                "four",
                "five",
                "six"
            };

            if (dice > 100)
            {
                return CustomResult.FromError("You may only roll up to 100 dice at a time");
            }
            else if (dice <= 0)
            {
                dice = 1;
            }

            string diceMessage = Context.User.Mention + " :game_die: You just rolled a ";
            string diceEmoji = "";
            int total = 0;

            Random rnd = new Random();
            for (int i=0; i < dice; i++)
            {
                int die = rnd.Next(1, 7);
                diceMessage += "**" + die + "** +" ;
                diceEmoji += ":" + emojis[die - 1] + ":";
                total += die;
            }
            diceMessage = diceMessage.Remove(diceMessage.Length - 2, 2);
            diceMessage += "!";
            await ReplyAsync(diceMessage + " " + diceEmoji);

            if (dice > 1)
            {
                string dice_stats = "`Total:   " + total + "`\n`Average: " + total / dice + "`";
                await ReplyAsync(dice_stats);
            }
            return CustomResult.FromSuccess();
        }

        [Command("pick")]
        [Alias("choose", "select")]
        [Summary("Pick from a list of options. Seperate options with ,")]
        public async Task Pick([Remainder] string optionsStr)
        {
            string[] options = optionsStr.Split(",");
            List<string> pickMessage = new List<string>()
            {
                "I'm in the mood for ",
                "",
                "Eeny, meeny, miny, moe. I pick ",
                "An obvious choice: ",
                "Do you even need to ask? The obvious answer is "
            };
            List<string> afterMessage = new List<string>()
            {
                " today.",
                ", I choose you!",
                ".",
                ", naturally.",
                "."
            };

            Random rdm = new Random();
            int x = rdm.Next(0, pickMessage.Count);
            int y = rdm.Next(0, options.Length);
            await ReplyAsync(Context.User.Mention + " " + pickMessage[x] + options[y].Trim() + afterMessage[x]);
        }

        [Command("8ball")]
        [Alias("eightball", "8-ball")]
        [Summary("Ask the magic 8ball something")]
        public async Task EightBall([Remainder] string query)
        {
            List<string> responses = new List<string>()
            {
                "It is certain.",
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
                "Very doubtful."
            };

            Random rnd = new Random();
            int rand = rnd.Next(0, 19);
            string emoji = ":negative_squared_cross_mark";

            if (rand < 10)
            {
                emoji = ":white_check_mark:";
            }
            else if (rand < 15)
            {
                emoji = ":question:";
            }
            await ReplyAsync(emoji + " " + Context.User.Mention + " " + responses[rand]);

        }
    }
}
