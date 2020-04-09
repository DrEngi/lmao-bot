using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Events
{
    public class ReadyEvent
    {
        LogService Log;
        MusicService Music;
        
        public ReadyEvent(DiscordShardedClient client, LogService log, MusicService music)
        {
            client.ShardReady += ShardReady;
            Log = log;
            Music = music;
        }

        private async Task ShardReady(DiscordSocketClient arg)
        {
            Log.LogString("Shard " + arg.ShardId + " online. " + arg.Guilds.Count + " servers.");
            if (arg.ShardId == await arg.GetRecommendedShardCountAsync() - 1)
            {
                Log.LogString("Bot ready. Activating music...");
                await Music.InitializeAsync();
            }
        }
    }
}
