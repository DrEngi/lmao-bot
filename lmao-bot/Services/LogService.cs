using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    public class LogService
    {
        private DiscordShardedClient Client;
        
        public LogService(DiscordShardedClient client)
        {
            Client = client;
            
            if (!Directory.Exists("logs/"))
            {
                Directory.CreateDirectory("logs/");
            }
            if (File.Exists("logs/latest.log"))
            {
                string newFile = $"logs/log-{DateTime.Now:MM-dd-yy H-mm-ss}.log";
                File.Move("logs/latest.log", newFile);
            }
        }
        
        public Task LogDiscord(LogMessage message)
        {
            Console.WriteLine($"[{message.Severity.ToString().ToUpper()}] [DISCORD] {message.Message}");

            File.AppendAllText("logs/latest.log", $"[{message.Severity.ToString().ToUpper()}] [DISCORD] {message.Message}" + Environment.NewLine);
            File.AppendAllText("logs/latest.log", $"{message.Exception}" + Environment.NewLine);
           
            return Task.CompletedTask;
        }

        public Task LogCommand(LogMessage message)
        {
            // Return an error message for async commands
            if (message.Exception is CommandException command)
            {
                // Don't risk blocking the logging task by awaiting a message send; ratelimits!?
                var _ = command.Context.Channel.SendMessageAsync($"Error: {command.Message}");
                Console.WriteLine("[ERROR] [COMMAND] " + command.Message);
                File.AppendAllText("logs/latest.log", "[INFO] " + message + Environment.NewLine);

                //Send information to exceptions channel: 711423990459006986
                Embed e = new EmbedBuilder()
                {
                    Title = "Bot Exception",
                    Description = $"{command.Message}",
                    Color = Color.Red,
                    Fields = new List<EmbedFieldBuilder>()
                    {
                        new EmbedFieldBuilder()
                        {
                            Name = "Server ID",
                            Value = command.Context.Guild.Id,
                            IsInline = true
                        },
                        new EmbedFieldBuilder()
                        {
                            Name = "User ID",
                            Value = command.Context.User.Id,
                            IsInline = true
                        },
                        new EmbedFieldBuilder()
                        {
                            Name = "Channel ID",
                            Value = command.Context.Channel.Id,
                            IsInline = false
                        }
                    },
                    Timestamp = DateTime.Now,
                    Footer = new EmbedFooterBuilder()
                    {
                        Text = "This will also be logged to the console and latest.log"
                    }
                }.Build();

                if (Client.CurrentUser.Id == 459432854821142529)
                {
                    //this is supremely hacky but just doing it for a temporary fix
                    if (message.Exception.InnerException.Message.Contains("403") || message.Exception.InnerException.Message.Contains("50013"))
                    {
                        //don't bother forwarding exceptions if they're because of permission issues
                        return Task.CompletedTask;
                    }
                    
                    var _1 = ((IMessageChannel)Client.GetChannel(711423990459006986)).SendMessageAsync(embed: e);
                    var _2 = ((IMessageChannel)Client.GetChannel(711423990459006986)).SendMessageAsync($"```{message.Exception}```");
                }   
            }
            return Task.CompletedTask;
        }

        public void LogString(string message)
        {
            Console.WriteLine("[INFO] " + message);
            File.AppendAllText("logs/latest.log", "[INFO] " + message + Environment.NewLine);
        }
    }
}
