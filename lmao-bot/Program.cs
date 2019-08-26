using Discord;
using Discord.Addons.Interactive;
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
        private BotConfig Config;

        public async Task MainAsync()
        {
            Console.WriteLine("Info Starting up lmao-bot v2");
            Client = new DiscordSocketClient();
            Config = JsonConvert.DeserializeObject<BotConfig>(File.ReadAllText("config.json"));

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
                .AddSingleton(new CommandService(new CommandServiceConfig { DefaultRunMode = RunMode.Async }))
                .AddSingleton<CommandHandlingService>()
                .AddSingleton<LogService>()                 //logging
                .AddSingleton(Config)                       //configuration
                .AddSingleton<DatabaseService>()            //database
                .AddSingleton<StatusService>()              //playing... status
                .AddSingleton<DBLService>()                 //discord bot list
                .AddSingleton<UrbanDictionaryService>()     //urban dictionary
                .AddSingleton<InteractiveService>()         //enables interactive commands
                .BuildServiceProvider();
        }
    }
}
