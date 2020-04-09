using Discord.WebSocket;
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
        
        public JoinedGuildEvent(DiscordShardedClient client, DatabaseService database)
        {
            Client = client;
            Database = database;
            Client.JoinedGuild += Client_JoinedGuild;
        }

        private async Task Client_JoinedGuild(SocketGuild arg)
        {
            await Database.GetServerSettings().CreateServerSettings((long)arg.Id);
        }
    }
}
