using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Events;
using lmao_bot.Services;
using Microsoft.Extensions.DependencyInjection;
using Newtonsoft.Json;
using System;
using System.IO;
using System.Threading.Tasks;

namespace lmao_bot
{
    class Program
    {
        static void Main(string[] args) => new Program().MainAsync().GetAwaiter().GetResult();

        private DiscordSocketClient Client;
        private Config Config;

        public async Task MainAsync()
        {
            Console.WriteLine("INFO Starting up lmao-bot v2");
            Client = new DiscordSocketClient();
            Config = JsonConvert.DeserializeObject<Config>(File.ReadAllText("config.json"));

            var services = ConfigureServices();
            await services.GetRequiredService<CommandHandlingService>().InitializeAsync(services);

            new LogEvent(services.GetRequiredService<LogService>(), Client, services.GetRequiredService<CommandService>());

            await Client.LoginAsync(TokenType.Bot, Config.token);
            await Client.StartAsync();

            await Task.Delay(-1);

        }

        private IServiceProvider ConfigureServices()
        {
            return new ServiceCollection()
                // Base
                .AddSingleton(Client)
                .AddSingleton<CommandService>()
                .AddSingleton<CommandHandlingService>()
                // Logging
                .AddSingleton<LogService>()
                // Extra
                .AddSingleton(Config)
                .AddSingleton<DatabaseService>()
                // Add additional services here...
                .BuildServiceProvider();
        }
    }

    class Config
    {
        public string token { get; set; }
    }
}
