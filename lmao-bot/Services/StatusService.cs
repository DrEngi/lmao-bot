using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Services
{
    public class StatusService
    {
        private string StatusText;
        private DateTime Maintenance;
        private DiscordSocketClient Client;

        public StatusService(DiscordSocketClient client)
        {
            Client = client;
            StatusText = "Starting up...";
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
    }
}
