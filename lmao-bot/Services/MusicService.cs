using Discord;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Victoria;

namespace lmao_bot.Services
{
    public class MusicService
    {
        BotConfig Config;
        DiscordShardedClient Client;
        LavaNode LavaNode;

        public MusicService(BotConfig config, DiscordShardedClient client)
        {
            this.Config = config;
            this.Client = client;
        }

        public async Task InitializeAsync()
        {
            LavaNode = new LavaNode(Client, config: new LavaConfig()
            {
                Hostname = Config.Lavalink.Hostname,
                Port = (ushort)Config.Lavalink.Port,
                Authorization = Config.Lavalink.Password,
                SelfDeaf = true
            });

            await LavaNode.ConnectAsync();
            await LavaNode.

            try
            {
                LavaPlayer player = await LavaNode.JoinAsync(Client.GetChannel(547246466733703168) as IVoiceChannel);
                var search = await LavaNode.SearchYouTubeAsync("avatar the last airbender");
                await player.PlayAsync(search.Tracks.FirstOrDefault());
            }
            catch (Exception ex)
            {

                throw;
            }
        }
    }
}
