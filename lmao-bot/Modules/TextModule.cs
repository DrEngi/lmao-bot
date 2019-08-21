using Discord.Commands;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class TextModule : ModuleBase
    {
        [Command("clap")]
        [Alias("clappify")]
        [Summary(":clap: Add :clap: some :clap: claps :clap: to :clap: your :clap: message. :clap:")]
        public async Task Clap([Remainder] string message)
        {
            string[] words = message.Split(" ");
            string response = ":clap: ";
            foreach (string word in words)
            {
                response = response + word + " :clap: ";
            }
            await ReplyAsync(response);
        }
    }
}
