﻿using Discord;
using Discord.Commands;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Models.UserSettings;
using lmao_bot.Services;
using System;
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
                LmaoBotServer serverSettings = await Database.GetServerSettings().GetServerSettings((long)Context.Guild.Id);
                if (new Random().Next(1, 100) <= serverSettings.BotSettings.ReplaceAssChance) await ReplyAsync(Context.User.Mention + " You appear to have misplaced your ass while laughing. Here is a replacement: :peach:");
                if (new Random().Next(1, 100) <= serverSettings.BotSettings.ReactChance) await Context.Message.AddReactionAsync(new Emoji("\U0001F351"));
            }
            await Database.GetUserSettings().IncrementLmaoCount((long)Context.User.Id);
        }

        [Command("count")]
        [Summary("Counts everytime you've said lmao or lmfao")]
        public async Task CountAss()
        {
            LmaoBotUser userSettings = await Database.GetUserSettings().GetUserSettings((long)Context.User.Id);
            if (userSettings.Settings.LmaoCount == 0) await ReplyAsync(Context.User.Mention + " You have yet to laugh your ass off");
            else if (userSettings.Settings.LmaoCount == 1) await ReplyAsync(Context.User.Mention + " You have laughed your ass off " + userSettings.Settings.LmaoCount + " time");
            else await ReplyAsync(Context.User.Mention + " You have laughed your ass off " + userSettings.Settings.LmaoCount + " times");
        }

        [Command("toggle")]
        [Summary("Toggle lmao-bot reaction settings in this server")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild)]
        public async Task ToggleReaction()
        {
            LmaoBotServer serverSettings = await Database.GetServerSettings().GetServerSettings((long)Context.Guild.Id);

            int newChance;

            if (serverSettings.BotSettings.ReplaceAssChance != 0)
            {
                await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, 0);
                await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, 0);
                newChance = 0;
            }
            else
            {
                await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, 100);
                await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, 100);
                newChance = 100;
            }

            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `" + newChance + "%`.");
        }

        [Command("on")]
        [Summary("Turns lmao-bot reactions on in this server")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task On()
        {
            await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, 100);
            await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, 100);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `100%`.");
        }

        [Command("off")]
        [Summary("Turns lmao-bot reactions off in this server.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Off()
        {
            await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, 0);
            await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, 0);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `0%`.");
        }

        [Command("lotto")]
        [Summary("Sets reaction chance to 1%.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Lotto()
        {
            await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, 1);
            await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, 1);
            await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `1%`.");
        }

        [Command("setass")]
        [Summary("Sets ass replacement chance to the specified percentage")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task<RuntimeResult> SetAss(int chance)
        {
            if (chance < 0 || chance > 100) 
            {
                return CustomResult.FromError("The chance must be between 0 and 100");
            }
            else
            {
                await Database.GetServerSettings().SetReplaceAssChance((long)Context.Guild.Id, chance);
                await ReplyAsync(Context.User.Mention + " You have set the ass replacement chance to `" + chance + "%`.");
                return CustomResult.FromSuccess();
            }
        }

        [Command("setreact")]
        [Summary("Sets react chance to the specified percentage")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group="Group")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server")]
        public async Task<RuntimeResult> SetReact(int chance)
        {
            if (chance < 0 || chance > 100)
            {
                return CustomResult.FromError("The chance must be between 0 and 100");
            }
            else
            {
                await Database.GetServerSettings().SetReactChance((long)Context.Guild.Id, chance);
                await ReplyAsync(Context.User.Mention + " You have set the react chance to  `" + chance + "%`.");
                return CustomResult.FromSuccess();
            }
        }
    }
}
