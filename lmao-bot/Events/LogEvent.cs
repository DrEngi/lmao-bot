using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Events
{
    public class LogEvent
    {
        LogService Log;

        public LogEvent(LogService logService, DiscordSocketClient client, CommandService commandService)
        {
            Log = logService;
            client.Log += LogMessage;
            commandService.Log += LogCommand;
        }

        public async Task LogMessage(LogMessage arg)
        {
            await Log.LogDiscord(arg);
        }

        public async Task LogCommand(LogMessage arg)
        {
            await Log.LogCommand(arg);
        }
    }
}
