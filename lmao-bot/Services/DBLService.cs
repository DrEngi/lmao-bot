using Discord.WebSocket;
using DiscordBotsList.Api;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    class DBLService
    {
        private DiscordBotListApi UnauthAPI;
        private AuthDiscordBotListApi AuthAPI;

        private LogService Log;
        private BotConfig Config;
        private DiscordShardedClient Client;

        public DBLService(LogService log, BotConfig config, DiscordShardedClient client)
        {
            Log = log;
            Config = config;
            Client = client;

            UnauthAPI = new DiscordBotListApi();
            if (config.Dbl != null) AuthAPI = new AuthDiscordBotListApi(client.CurrentUser.Id, Config.Dbl);
            Log.LogString("Connected to DBL");
        }

        /// <summary>
        /// Checks if the user has voted for the bot
        /// </summary>
        /// <param name="id">The ID of the user to check</param>
        /// <returns>True if the user voted, false if not</returns>
        public async Task<bool> CheckUser(ulong id)
        {
            if (AuthAPI == null) return true;
            return await AuthAPI.HasVoted(id);
        }

        /// <summary>
        /// Updates the server statistics for DBL
        /// </summary>
        /// <param name="guildCount">The number of servers the bot is in</param>
        public async void UpdateStats(int guildCount)
        {
            if (AuthAPI == null) return;
            await AuthAPI.UpdateStats(guildCount);
        }
    }
}
