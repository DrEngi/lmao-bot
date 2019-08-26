using Discord;
using Discord.Commands;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class DevModule : ModuleBase
    {
        public DatabaseService Database;

        public DevModule(DatabaseService database)
        {
            Database = database;
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

        public async Task Announce()
        {
            //TODO: Announce command
        }

        [Command("changemaint")]
        [Alias("setmaint")]
        [Summary("Inform users of when the bot will be down for maintenance")]
        public async Task ChangeMaintenance()
        {
            
        }
    }
}
