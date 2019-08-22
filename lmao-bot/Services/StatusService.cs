using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Services
{
    public class StatusService
    {
        private string statusText;
        private DiscordSocketClient Client;

        public StatusService(DiscordSocketClient client)
        {
            Client = client;
            statusText = "Starting up...";
            Client.SetActivityAsync(new Discord.Game(statusText));
        }
    }
}
