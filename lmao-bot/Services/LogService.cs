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
        public LogService()
        {
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
            Console.WriteLine($"[{message.Severity.ToString().ToUpper()}] {message.Message}");
            File.AppendAllText("logs/latest.log", $"[{message.Severity.ToString().ToUpper()}] {message.Message}" + Environment.NewLine);
            File.AppendAllText("logs/latest.log", $"{message.Exception}" + Environment.NewLine);
            Console.WriteLine(message.Exception + Environment.NewLine);
            return Task.CompletedTask;
        }

        public Task LogCommand(LogMessage message)
        {
            // Return an error message for async commands
            if (message.Exception is CommandException command)
            {
                // Don't risk blocking the logging task by awaiting a message send; ratelimits!?
                var _ = command.Context.Channel.SendMessageAsync($"Error: {command.Message}");
                Console.WriteLine("[ERROR] " + command.Message);
                File.AppendAllText("logs/latest.log", "[INFO] " + message + Environment.NewLine);
            }

            Console.WriteLine(message.Severity + " " + message.Message);
            return Task.CompletedTask;
        }

        public void LogString(string message)
        {
            Console.WriteLine("[INFO] " + message);
            File.AppendAllText("logs/latest.log", "[INFO] " + message + Environment.NewLine);
        }
    }
}
