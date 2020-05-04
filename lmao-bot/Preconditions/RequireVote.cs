using Discord.Commands;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Preconditions
{
    public class RequireVote : PreconditionAttribute
    {
        public override async Task<PreconditionResult> CheckPermissionsAsync(ICommandContext context, CommandInfo command, IServiceProvider services)
        {
            DBLService dbl = (DBLService) services.GetService(typeof(DBLService));
            if (await dbl.CheckUser(context.User.Id))
            {
                return await Task.FromResult(PreconditionResult.FromSuccess());
            }
            else
            {
                return await Task.FromResult(PreconditionResult.FromError("You must have voted to use this command. See `lmao vote` for more info."));
            }
        }
    }
}
