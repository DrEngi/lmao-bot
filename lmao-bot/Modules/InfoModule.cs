using Discord;
using Discord.Commands;
using lmao_bot.Services;
using System;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class InfoModule : ModuleBase
    {
        private APIService Database;

        public InfoModule(APIService service)
        {
            Database = service;
        }

        [Command("prefix")]
        [Summary("Change the bot prefix for this server")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild)]
        public async Task Prefix()
        {

        }
    }
}