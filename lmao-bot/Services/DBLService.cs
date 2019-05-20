using Discord.WebSocket;
using DiscordBotsList.Api;
using lmao_bot.Models;
using System;
using System.Collections.Generic;
using System.Text;

namespace lmao_bot.Services
{
    class DBLService
    {
        DiscordBotListApi UnauthAPI;
        AuthDiscordBotListApi AuthAPI;

        LogService Log;
        Config Config;
        DiscordSocketClient Client;

        public DBLService(LogService log, Config config, DiscordSocketClient client)
        {
            Log = log;
            Config = config;
            Client = client;

            UnauthAPI = new DiscordBotListApi();
            AuthAPI = new AuthDiscordBotListApi(client.CurrentUser.Id, Config.Dbl);
            Log.LogString("Connected to DBL");
        }
    }
}
