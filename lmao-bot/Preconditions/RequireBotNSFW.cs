using Discord.Commands;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Preconditions
{
    public class RequireBotNSFW : PreconditionAttribute
    {
        public override async Task<PreconditionResult> CheckPermissionsAsync(ICommandContext context, CommandInfo command, IServiceProvider services)
        {
            DatabaseService db = (DatabaseService)services.GetService(typeof(DatabaseService));
            LmaoBotServer settings = await db.GetServerSettings().GetServerSettings((long)context.Guild.Id);
            if (settings.BotSettings.AllowNSFW)
            {
                return await Task.FromResult(PreconditionResult.FromSuccess());
            }
            else
            {
                return await Task.FromResult(PreconditionResult.FromError("The bot is not allowed to use NSFW commands in this server. See `lmao nsfwtoggle` for more info."));
            }
        }
    }
}
