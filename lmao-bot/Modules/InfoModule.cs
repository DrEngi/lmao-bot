using Discord;
using Discord.Commands;
using lmao_bot.Services;
using lmaocore.Models.ServerSettings;
using System;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class InfoModule : ModuleBase
    {
        private DatabaseService Database;

        public InfoModule(DatabaseService service)
        {
            Database = service;
        }

        [Command("prefix")]
        [Summary("Change the bot prefix for this server")]
        [RequireContext(ContextType.Guild)]
        public async Task Prefix()
        {
            await ReplyAsync(Context.User.Mention + " My current prefix for " + Context.Guild.Name + " is " + await Database.GetPrefix((long)Context.Guild.Id) + ".");
        }

        [Command("prefix")]
        [Alias("setprefix")]
        [Summary("Change the bot prefix for this server")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group = "Group")]
        [RequireContext(ContextType.Guild)]
        public async Task SetPrefix(string prefix)
        {
            ServerSettings settings = await Database.GetServerSettings((long)Context.Guild.Id);
            settings.BotSettings.CommandPrefix = prefix;

            await Database.SaveServerSettings(settings, new SaveServerSettingsOptions()
            {
                BotSettingsOptions = new SaveBotSettingsOptions()
                {
                    UpdateCommandPrefix = true,
                }
            });
            await ReplyAsync(Context.User.Mention + " My command prefix for " + Context.Guild.Name + " is now " + prefix + ".");
        }
    }
}