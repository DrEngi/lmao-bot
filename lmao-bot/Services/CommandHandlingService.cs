using Discord;
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

        private Dictionary<ulong, DateTime> tempRateLimits = new Dictionary<ulong, DateTime>();

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

                if (tempRateLimits.ContainsKey(context.User.Id))
                {
                    if (DateTime.Now.Subtract(tempRateLimits[context.User.Id]) < new TimeSpan(0, 0, 3))
                    {
                        Console.WriteLine("rate limits activated on " + context.User.Username);
                        return;
                    }
                    else
                    {
                        tempRateLimits[context.User.Id] = DateTime.Now;
                    }
                }
                else
                {
                    tempRateLimits.Add(context.User.Id, DateTime.Now);
                }

                using (IDisposable ITyping = context.Channel.EnterTypingState())
                {
                    await Commands.ExecuteAsync(context, argPos, Provider);
                }
            }
            else if (message.Content.ToLower().Contains("lmao") || message.Content.ToLower().Contains("lmfao"))
            {
                SocketCommandContext context;
                if (guild != null) context = new SocketCommandContext(Discord.GetShardFor(guild), message);
                else context = new SocketCommandContext(Discord.GetShard(0), message);

                if (tempRateLimits.ContainsKey(context.User.Id))
                {
                    if (DateTime.Now.Subtract(tempRateLimits[context.User.Id]) < new TimeSpan(0, 0, 3))
                    {
                        Log.LogString("rate limits activated on " + context.User.Username);
                        //293855081596452866 712812620952109117

                        return;
                    }
                    else
                    {
                        tempRateLimits[context.User.Id] = DateTime.Now;
                    }
                }
                else
                {
                    tempRateLimits.Add(context.User.Id, DateTime.Now);
                }

                //Console.WriteLine("command executing: " + context.Message.Content + " by " + context.Message.Author + " in " + context.Message.Channel);

                //Message is not a command but contains lmao so we're gonna replace some asses          
                using (IDisposable ITyping = context.Channel.EnterTypingState())
                {
                    await Commands.ExecuteAsync(context, "replaceass", Provider);
                }
                return;
            }
        }
    }
}
