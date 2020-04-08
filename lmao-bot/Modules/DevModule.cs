using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class DevModule : ModuleBase
    {
        private DatabaseService Database;
        private StatusService Status;
        private DiscordSocketClient Client;

        public DevModule(DatabaseService database, StatusService status, DiscordSocketClient client)
        {
            Database = database;
            Status = status;
            Client = client;
        }

        [Command("uptime")]
        [Alias("timeup", "online")]
        [Summary("Displays the uptime for the bot")]
        public async Task Uptime()
        {
            var embed = new EmbedBuilder
            {
                Title = "Bot Uptime",
                Color = Color.DarkMagenta,
                Description = Database.UptimeWatch.Elapsed.ToString(@"dd\.hh\:mm\:ss"),
            }.Build();

            await ReplyAsync(embed: embed);
        }

        [Command("ping")]
        [Alias("latency")]
        [Summary("Test bot response time")]
        public async Task Ping()
        {
            await ReplyAsync("Pong!");
        }

        [Command("announce")]
        [Summary("Announce a message to the world at large")]
        [RequireBotDeveloper()]
        public async Task<RuntimeResult> Announce(String message)
        {
            // THIS IS BAD PRACTICE DON'T DO THIS
            // TODO: Move this to a service or somewhere not here, so if the bot crashes we can continue automatically.
            _ = Task.Run(() =>
            {
                Thread.Sleep(5000);
                foreach (SocketGuild g in this.Client.Guilds)
                {
                    var embed = new EmbedBuilder
                    {
                        Title = "Bot Announcement",
                        Color = Color.Orange,
                        Description = message,
                        Footer = new EmbedFooterBuilder
                        {
                            Text = DateTime.Now.ToShortDateString()
                        }
                    }.Build();

                    g.DefaultChannel.SendMessageAsync(embed: embed);
                    Thread.Sleep(5000);
                }
            });
            return CustomResult.FromSuccess("Announcement will begin in 10 seconds.");
        }

        [Command("changemaint")]
        [Alias("setmaint")]
        [Summary("Inform users of when the bot will be down for maintenance")]
        [RequireBotDeveloper()]
        public async Task<RuntimeResult> ChangeMaintenance(DateTime time)
        {
            Status.SetMaintenance(time);
            //await ReplyAsync(Context.User.Mention + " You have set the react chance to  `" + chance + "%`.");
            return CustomResult.FromSuccess($"Maintenance set to {time.ToShortTimeString()}");

        }

        [Command("disconnectguild")]
        [Summary("Disconnects a given guild from the music system")]
        [RequireBotDeveloper()]
        public async Task<RuntimeResult> DisconnectGuild(long ServerID)
        {
            //TODO: Implement disconnect guild when music is done.
            return CustomResult.FromSuccess();
        }
    }
}
