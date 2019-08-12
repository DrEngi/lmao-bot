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
            Console.WriteLine("Info Starting up lmao-bot v2");
            Client = new DiscordSocketClient();
            Config = JsonConvert.DeserializeObject<Config>(File.ReadAllText("config.json"));

            var services = ConfigureServices();
            await services.GetRequiredService<CommandHandlingService>().InitializeAsync(services);

            new LogEvent(services.GetRequiredService<LogService>(), Client, services.GetRequiredService<CommandService>());

            await Client.LoginAsync(TokenType.Bot, Config.Token);
            await Client.StartAsync();

            await Task.Delay(-1);
        }

        private IServiceProvider ConfigureServices()
        {
            /**
             * This looks complicated but I promise it's not. We don't want to create new instances
             * of these classes every time we run a command, so we call them Singletons (that way, they're
             * only created once when they're needed and then maintained throughout the lifetime of the
             * application)
             **/        
            return new ServiceCollection()
                .AddSingleton(Client)                       //base discord services
                .AddSingleton<CommandService>()
                .AddSingleton<CommandHandlingService>()
                .AddSingleton<LogService>()                 //logging
                .AddSingleton(Config)                       //configuration
                .AddSingleton<APIService>()            //database
                .AddSingleton<DBLService>()                 //discord bot list
                .BuildServiceProvider();
        }
    }
}
