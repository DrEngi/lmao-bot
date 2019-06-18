using Discord;
using Discord.Commands;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class PeachModule : ModuleBase
    {
        private DatabaseService Database;

        public PeachModule(DatabaseService database)
        {
            Database = database;
        }

        [Command("replaceass")]
        [Summary("Replaces the ass you just lost")]
        public async Task ReplaceAss()
        {
            //We don't want to get server settings of a DM.
            if (Context.Channel is IDMChannel)
            {
                await ReplyAsync(Context.User.Mention + " You appear to have misplaced your ass while laughing. Here is a replacement: :peach:");
                
            }
            else
            {
                lmaocore.Models.ServerSettings.Server serverSettings = await Database.GetServerSettings((long)Context.Guild.Id);
                if (new Random().Next(1, 100) <= serverSettings.BotSettings.ReplaceAssChance) await ReplyAsync(Context.User.Mention + " You appear to have misplaced your ass while laughing. Here is a replacement: :peach:");
                if (new Random().Next(1, 100) <= serverSettings.BotSettings.ReactChance) await Context.Message.AddReactionAsync(new Emoji("\U0001F351"));
            }
            await Database.UpdateLmaoCount((long)Context.User.Id);
        }

        [Command("count")]
        [Summary("Counts everytime you've said lmao or lmfao")]
        public async Task CountAss()
        {
            lmaocore.Models.UserSettings.UserSettings userSettings = await Database.GetUserSettings((long)Context.User.Id);
            if (userSettings.Settings.LmaoCount == 0) await ReplyAsync(Context.User.Mention + " You have yet to laugh your ass off");
            else if (userSettings.Settings.LmaoCount == 1) await ReplyAsync(Context.User.Mention + " You have laughed your ass off " + userSettings.Settings.LmaoCount + " time");
            else await ReplyAsync(Context.User.Mention + " You have laughed your ass off " + userSettings.Settings.LmaoCount + " times");
        }

        [Command("toggle")]
        [Summary("Toggle lmao-bot reaction settings in this server")]
        [RequireContext(ContextType.Guild)]
        public async Task ToggleReaction()
        {
            lmaocore.Models.ServerSettings.Server serverSettings = await Database.GetServerSettings((long)Context.Guild.Id);
            int newChance = await Database.SetAss(serverSettings, -1);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `" + newChance + "%`.");
        }

        [Command("on")]
        [Summary("Toggles lmao-bot reactions on in this server")]
        [RequireContext(ContextType.Guild)]
        public async Task On()
        {
            lmaocore.Models.ServerSettings.Server serverSettings = await Database.GetServerSettings((long)Context.Guild.Id);
            await Database.SetAss(serverSettings, 100);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `100%`.");
        }

        [Command("off")]
        [Summary("Toggles lmao-bot reactions on in this server")]
        [RequireContext(ContextType.Guild)]
        public async Task Off()
        {
            lmaocore.Models.ServerSettings.Server serverSettings = await Database.GetServerSettings((long)Context.Guild.Id);
            await Database.SetAss(serverSettings, 0);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `0%`.");
        }
    }
}
