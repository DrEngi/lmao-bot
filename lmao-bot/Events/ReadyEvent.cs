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
        StatusService Status;

        public ReadyEvent(DiscordShardedClient client, LogService log, MusicService music, StatusService status)
        {
            client.ShardReady += ShardReady;
            Log = log;
            Music = music;
            Status = status;
        }

        private async Task ShardReady(DiscordSocketClient arg)
        {
            Log.LogString("Shard " + arg.ShardId + " online. " + arg.Guilds.Count + " servers.");
            Status.SetToServerCount();
            //TODO: We need a better way of noting when a bot is completely ready
            if (arg.ShardId == await arg.GetRecommendedShardCountAsync() - 1)
            {
                Log.LogString("Bot ready.");
                
                //TODO: Uncomment this
                //await Music.InitializeAsync();
            }
        }
    }
}
