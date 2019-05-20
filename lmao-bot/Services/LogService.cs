using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Services
{
    public class LogService
    {
        public Task LogDiscord(LogMessage message)
        {
            Console.WriteLine(message.Severity + " " + message.Message);
            return Task.CompletedTask;
        }

        public Task LogCommand(LogMessage message)
        {
            // Return an error message for async commands
            if (message.Exception is CommandException command)
            {
                // Don't risk blocking the logging task by awaiting a message send; ratelimits!?
                var _ = command.Context.Channel.SendMessageAsync($"Error: {command.Message}");
            }

            Console.WriteLine(message.Severity + " " + message.Message);
            return Task.CompletedTask;
        }

        public void LogString(string message)
        {
            Console.WriteLine("INFO " + message);
        }
    }
}
