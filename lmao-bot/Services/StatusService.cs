using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    public class StatusService
    {
        private string StatusText;
        private DateTime Maintenance;
        private DiscordShardedClient Client;

        public StatusService(DiscordShardedClient client)
        {
            Client = client;
            StatusText = "Running rewerite test!";
            Client.SetActivityAsync(new Discord.Game(StatusText));
        }

        private void SetStatusText(string text)
        {
            StatusText = text;
            Client.SetActivityAsync(new Discord.Game(text));
        }

        public void SetToServerCount()
        {
            this.SetStatusText($"lmao help | {Client.Guilds.Count} servers");
        }

        public void SetMaintenance(DateTime time)
        {
            this.Maintenance = time;
            this.SetStatusText($"lmao help | Maint. @ {time.ToShortTimeString()}");
        }
    }
}
