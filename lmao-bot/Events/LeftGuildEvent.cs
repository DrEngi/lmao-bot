using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Events
{
    public class LeftGuildEvent
    {
        private DiscordShardedClient Client;
        private DatabaseService Database;
        private LogService Log;
        private StatusService Status;

        public LeftGuildEvent(DiscordShardedClient client, DatabaseService database, LogService log, StatusService status)
        {
            Client = client;
            Database = database;
            Log = log;
            Status = status;
            Client.LeftGuild += Client_LeftGuild;
        }

        private async Task Client_LeftGuild(SocketGuild arg)
        {
            Log.LogInfo($"Server left :( Total servers now at {Client.Guilds.Count}");
            await Database.GetServerSettings().DeleteServerSettings((long)arg.Id);
            Status.SetToServerCount();
        }
    }
}
