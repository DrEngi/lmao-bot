using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Attributes;
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    class CommandHandlingService
    {
        private readonly DiscordSocketClient Discord;
        private readonly CommandService Commands;
        private readonly DatabaseService Database;
        private IServiceProvider Provider;

        public CommandHandlingService(IServiceProvider provider, DiscordSocketClient client, CommandService commands, DatabaseService database)
        {
            Discord = client;
            Commands = commands;
            Provider = provider;
            Database = database;

            Discord.MessageReceived += Discord_MessageReceived;
            Commands.CommandExecuted += Commands_CommandExecuted;
        }

        private async Task Commands_CommandExecuted(Optional<CommandInfo> command, ICommandContext context, IResult result)
        {
            if (!string.IsNullOrEmpty(result?.ErrorReason))
            {
                if (result?.Error == CommandError.UnknownCommand && (context.Message.Content.Contains("lmao") || context.Message.Content.Contains("lmfao")))
                {
                    await Commands.ExecuteAsync(context, "replaceass", Provider);
                    return;
                }

                var embed = new EmbedBuilder
                {
                    Title = "Command Error",
                    Color = Color.Red,
                    Description = result.ErrorReason,
                    Footer = new EmbedFooterBuilder
                    {
                        Text = "Unexpected? Visit lmao support for help"
                    }
                }.Build();
                await context.Channel.SendMessageAsync(embed: embed);
            }

            // ...or even log the result (the method used should fit into
            // your existing log handler)
            var commandName = command.IsSpecified ? command.Value.Name : "A command";
            /*
            await _log.LogAsync(new LogMessage(LogSeverity.Info,
                "CommandExecution",
                $"{commandName} was executed at {DateTime.UtcNow}."));
            */
        }

        public async Task InitializeAsync(IServiceProvider provider)
        {
            Provider = provider;
            await Commands.AddModulesAsync(Assembly.GetEntryAssembly(), Provider);
        }

        private async Task Discord_MessageReceived(SocketMessage rawMessage)
        {
            // Ignore system messages and messages from bots
            if (!(rawMessage is SocketUserMessage message)) return;
            if (message.Source != MessageSource.User) return;

            int argPos = 0;
            //TODO: Catch lmfao and custom prefixes for server
            if ((message.HasMentionPrefix(Discord.CurrentUser, ref argPos) || message.HasStringPrefix("lmao", ref argPos)) && !message.HasStringPrefix("replaceass", ref argPos))
            {
                //Message is a command
                var context = new SocketCommandContext(Discord, message);
                var result = await Commands.ExecuteAsync(context, argPos, Provider);
            }
            else if (message.Content.Contains("lmao") || message.Content.Contains("lmfao"))
            {
                //Message is not a command but contains lmao so we're gonna replace some asses
                var context = new SocketCommandContext(Discord, message);
                await Commands.ExecuteAsync(context, "replaceass", Provider);
                return;
            }
        }
    }
}
