using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Preconditions;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    [RequireBotDeveloper(ErrorMessage = "NSFW is not implemented yet, but we're working on it!")]
    public class NSFWModule: ModuleBase
    {
        private DatabaseService Database;
        private DiscordShardedClient Client;

        public NSFWModule(DatabaseService service, DiscordShardedClient client)
        {
            Database = service;
            Client = client;
        }

        private Embed SearchReddit(string sub)
        {
            //TODO: Parse reddit with flurl.
            return null;
        }

        [Command("nsfwtoggle")]
        [Alias("togglensfw")]
        [Summary("Toggles NSFW commands for your server")]
        [RequireUserPermission(Discord.ChannelPermission.ManageMessages)]
        [RequireContext(ContextType.Guild)]
        public async Task ToggleNSFW()
        {
            LmaoBotServer settings = await Database.GetServerSettings().GetServerSettings((long)Context.Guild.Id);
            bool isEnabled = !settings.BotSettings.AllowNSFW;
            await Database.GetServerSettings().SetAllowNSFW((long)Context.Guild.Id, isEnabled);
            if (isEnabled) await ReplyAsync("NSFW Commands have now been enabled for your guild. :smirk:");
            else await ReplyAsync("NSFW Commands are now disabled for your guild.");
        }

        [Command("gonewild")]
        [RequireNsfw(ErrorMessage = "Whoa-ho-ho-ho, hold your horses. This command only works in NSFW channels.")]
        [RequireContext(ContextType.Guild)]
        [RequireVote]
        [RequireBotNSFW]
        public async Task GoneWild()
        {
            await ReplyAsync(embed: this.SearchReddit("gonewild"));
        }

        [Command("ladybonersgw")]
        [RequireNsfw(ErrorMessage = "Whoa-ho-ho-ho, hold your horses. This command only works in NSFW channels.")]
        [RequireContext(ContextType.Guild)]
        [RequireVote]
        [RequireBotNSFW]
        public async Task LBG()
        {
            await ReplyAsync(embed: this.SearchReddit("ladybonersgw"));
        }

        [Command("gonewildmale")]
        [RequireNsfw(ErrorMessage = "Whoa-ho-ho-ho, hold your horses. This command only works in NSFW channels.")]
        [RequireContext(ContextType.Guild)]
        [RequireVote]
        [RequireBotNSFW]
        public async Task GoneWildMale()
        {
            await ReplyAsync(embed: this.SearchReddit("gonewildmale"));
        }

        [Command("thighhighs")]
        [RequireNsfw(ErrorMessage = "Whoa-ho-ho-ho, hold your horses. This command only works in NSFW channels.")]
        [RequireContext(ContextType.Guild)]
        [RequireVote]
        [RequireBotNSFW]
        public async Task ThighHighs()
        {
            await ReplyAsync(embed: this.SearchReddit("thighhighs"));
        }
    }
}
