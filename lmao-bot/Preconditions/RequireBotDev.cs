using System;
using System.Threading.Tasks;
using Discord.Commands;
using Discord.WebSocket;

public class RequireBotDeveloper : PreconditionAttribute
{
    public override Task<PreconditionResult> CheckPermissionsAsync(ICommandContext context, CommandInfo command, IServiceProvider services)
    {
        if (context.User.Id == 257203526390906880 ||
            context.User.Id == 210220782012334081 ||
            context.User.Id == 300763778608267266)
        {
            return Task.FromResult(PreconditionResult.FromSuccess());
        }
        else
        {
            return Task.FromResult(PreconditionResult.FromError("You must be a bot developer to use this command"));
        }
    }
}