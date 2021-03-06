﻿using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Events
{
    public class JoinedGuildEvent
    {
        private DiscordShardedClient Client;
        private DatabaseService Database;
        private LogService Log;
        private StatusService Status;
        
        public JoinedGuildEvent(DiscordShardedClient client, DatabaseService database, LogService log, StatusService status)
        {
            Client = client;
            Database = database;
            Log = log;
            Status = status;
            Client.JoinedGuild += Client_JoinedGuild;
        }

        private async Task Client_JoinedGuild(SocketGuild arg)
        {
            Log.LogString($"New server! {arg.Name} with {arg.MemberCount} members! Total servers now at {Client.Guilds.Count}");
            await Database.GetServerSettings().CreateServerSettings((long)arg.Id);
            Status.SetToServerCount();
        }
    }
}
