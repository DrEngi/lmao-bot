using Discord.Commands;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class PeachModule : ModuleBase
    {
        [Command("replaceass")]
        [Summary("Replaces the ass you just lost")]
        public async Task ReplaceAss()
        {
            await ReplyAsync(Context.User.Mention + " You appear to have misplaced your ass while laughing. Here is a replacement: :peach:");
        }
    }
}
