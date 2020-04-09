﻿using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;
using System.Diagnostics;

namespace lmao_bot.Services
{
    class CommandHandlingService
    {
        private readonly DiscordShardedClient Discord;
        private readonly CommandService Commands;
        private readonly DatabaseService Database;
        private readonly LogService Log;
        private IServiceProvider Provider;

        public CommandHandlingService(IServiceProvider provider, DiscordShardedClient client, CommandService commands, DatabaseService database, LogService log)
        {
            Discord = client;
            Commands = commands;
            Provider = provider;
            Database = database;
            Log = log;

            Discord.MessageReceived += Discord_MessageReceived;
            Commands.CommandExecuted += Commands_CommandExecuted;
        }

        private async Task Commands_CommandExecuted(Optional<CommandInfo> command, ICommandContext context, IResult result)
        {
            if (result is CustomResult)
            {
                if (!string.IsNullOrEmpty(result?.ErrorReason))
                {
                    if (result.IsSuccess)
                    {
                        var embedSuccess = new EmbedBuilder
                        {
                            Title = "Command Finished",
                            Color = Color.Green,
                            Description = result.ErrorReason,
                            Footer = new EmbedFooterBuilder
                            {
                                Text = "Unexpected? Visit lmao support for help"
                            }
                        }.Build();
                        await context.Channel.SendMessageAsync(embed: embedSuccess);
                    }
                    else
                    {
                        //We called this error ourselves.
                        var embed = new EmbedBuilder
                        {
                            Title = "Command Error",
                            Color = Color.DarkBlue,
                            Description = result.ErrorReason,
                            Footer = new EmbedFooterBuilder
                            {
                                Text = "Unexpected? Visit lmao support for help"
                            }
                        }.Build();
                        await context.Channel.SendMessageAsync(embed: embed);
                    }
                }
                else if (result.IsSuccess)
                {
                    //TODO: Uncomment this
                    //if (command.IsSpecified) await Database.UpdateUsageCount(command.Value.Name);
                    //else Log.LogString("Command result was success but CommandInfo object not included?");
                }
                
                return;
            }


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
            else if (result.IsSuccess)
            {
                //TODO: Uncomment this
                //if (command.IsSpecified) await Database.UpdateUsageCount(command.Value.Name);
                //else Log.LogString("Command result was success but CommandInfo object not included?");
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
            string prefix = null;
            IGuild guild = null;

            if (rawMessage.Channel is IGuildChannel)
            {
                //Message being sent in a guild
                IGuildChannel channel = (IGuildChannel)rawMessage.Channel;
                prefix = await Database.GetPrefix((long)channel.GuildId);
                guild = channel.Guild;
            }
            else if (rawMessage.Channel is IDMChannel)
            {
                //Message being sent in a DM
                prefix = "lmao";
            }
            else Log.LogString("Unknown Channel Type");


            if (message.HasMentionPrefix(Discord.CurrentUser, ref argPos) || message.HasStringPrefix(prefix + " ", ref argPos))
            {
                if (message.HasStringPrefix("replaceass", ref argPos)) return;
                //Message is a command
                
                SocketCommandContext context;
                if (guild != null) context = new SocketCommandContext(Discord.GetShardFor(guild), message);
                else context = new SocketCommandContext(Discord.GetShard(0), message);

                await Commands.ExecuteAsync(context, argPos, Provider);
            }
            else if (message.Content.ToLower().Contains("lmao") || message.Content.ToLower().Contains("lmfao"))
            {
                SocketCommandContext context;
                if (guild != null) context = new SocketCommandContext(Discord.GetShardFor(guild), message);
                else context = new SocketCommandContext(Discord.GetShard(0), message);

                //Message is not a command but contains lmao so we're gonna replace some asses
                await Commands.ExecuteAsync(context, "replaceass", Provider);
                return;
            }
        }
    }
}
