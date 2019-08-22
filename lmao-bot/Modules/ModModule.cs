using Discord;
using Discord.Addons.Interactive;
using Discord.Commands;
using lmao_bot.Events;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Timers;

namespace lmao_bot.Modules
{
    public class ModModule : InteractiveBase
    {
        [Command("purge")]
        [Alias("clear", "clean", "prune", "obliterate")]
        [Summary("Remove a bunch of messages from your channel")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group = "Group")]
        [RequireBotPermission(GuildPermission.ManageMessages)]
        public async Task<RuntimeResult> Purge(int messageCount)
        {
            if (messageCount > 100) return CustomResult.FromError("You cannot purge more than 100 messages at a time");
            // Check if the amount provided by the user is positive.
            if (messageCount <= 0) return CustomResult.FromError("You cannot purge a negative number");
            var messages = await Context.Channel.GetMessagesAsync(messageCount).FlattenAsync();
            var filteredMessages = messages.Where(x => (DateTimeOffset.UtcNow - x.Timestamp).TotalDays <= 14);

            // Get the total amount of messages.
            var count = filteredMessages.Count();

            // Check if there are any messages to delete.
            if (count == 0) return CustomResult.FromError("Nothing to delete.");
            else
            {
                await (Context.Channel as ITextChannel).DeleteMessagesAsync(filteredMessages);
                await ReplyAndDeleteAsync($"Done. Removed {count} {(count > 1 ? "messages" : "message")}.");
                return CustomResult.FromSuccess();
            }
        }

        [Command("mute")]
        [Alias("silence", "shush")]
        [Summary("Mute a user in your server")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group = "Group")]
        [RequireBotPermission(GuildPermission.ManageMessages)]
        public async Task<RuntimeResult> Mute(IGuildUser user, TimeSpan? duration = null)
        {
            try
            {
                if (user.Id == Context.Client.CurrentUser.Id) return CustomResult.FromError($"Silly {Context.User.Mention}, I can't mute myself!");
                if (!duration.HasValue)
                {
                    var channel = Context.Guild.GetChannel(Context.Channel.Id);
                    await channel.AddPermissionOverwriteAsync(user, new OverwritePermissions(sendMessages: PermValue.Deny));
                    return CustomResult.FromSuccess($"{user.Mention} was permanently muted in {Context.Channel.Name} by {Context.User.Mention}.");
                }
                else
                {
                    var channel = Context.Guild.GetChannel(Context.Channel.Id);
                    await channel.AddPermissionOverwriteAsync(user, new OverwritePermissions(sendMessages: PermValue.Deny));
                    string timeString = "";
                    if (duration.Value.Hours != 0) timeString += $"{duration.Value.Hours} hours, ";
                    if (duration.Value.Minutes != 0) timeString += $"{duration.Value.Minutes} minutes, ";
                    if (duration.Value.Seconds != 0) timeString += $"{duration.Value.Seconds} seconds";

                    _ = Task.Run(async () =>
                    {
                        Thread.Sleep((int)duration.Value.TotalMilliseconds);
                        await channel.RemovePermissionOverwriteAsync(user);
                        Embed e = new EmbedBuilder()
                        {
                            Title = "Notice",
                            Description = $"{ user.Mention } is no longer muted.",
                            Color = Color.Orange,
                            Footer = new EmbedFooterBuilder()
                            {
                                Text = $"Originally muted by {Context.User.Username}"
                            }
                        }.Build();
                        await ReplyAsync(embed: e);
                    });
                    return CustomResult.FromSuccess($"{user.Mention} was muted in {Context.Channel.Name} by {Context.User.Mention} for {timeString}.");
                }
            }
            catch (Exception ex)
            {
                await ReplyAsync(ex.ToString());
                await ReplyAsync(ex.StackTrace);
                throw;
            }
        }

        [Command("ban")]
        [Summary("Ban a user from your server")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.BanMembers, Group = "Group")]
        [RequireBotPermission(GuildPermission.BanMembers)]
        public async Task<RuntimeResult> Ban(IGuildUser user, [Remainder]string reason = "")
        {
            if (user.Id == Context.Client.CurrentUser.Id) return CustomResult.FromError($"Silly { Context.User.Mention}, I can't ban myself!");
            if (user.Id == Context.User.Id) return CustomResult.FromError($"{ Context.User.Mention}, you can't ban yourself");

            string reasonString = (reason.Length == 0) ? "No reason given." : reason;
            Embed announceE = new EmbedBuilder()
            {
                Title = "User Banned",
                Color = Color.Green,
                Description = $"{user.Mention} was banned from the server.",
                Fields = new List<EmbedFieldBuilder>()
                {
                    new EmbedFieldBuilder()
                    {
                        Name = "Reason",
                        Value = reasonString
                    }
                }
            }.Build();

            Embed dmE = new EmbedBuilder()
            {
                Title = $"You have been banned from {Context.Guild.Name} by {Context.User.Username}",
                Color = Color.Red,
                Description = reasonString,
                Timestamp = DateTime.Now
            }.Build();

            await (await user.GetOrCreateDMChannelAsync()).SendMessageAsync(embed: dmE);
            await user.BanAsync(reason: reasonString);
            await ReplyAsync(embed: announceE);
            return CustomResult.FromSuccess();
        }

        /*
        [Command("tempban")]
        [Alias("tban")]
        [Summary("Temporarily a user from your server")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.BanMembers, Group = "Group")]
        [RequireBotPermission(GuildPermission.BanMembers)]
        public async Task<RuntimeResult> TempBan(IGuildUser user, TimeSpan duration, [Remainder]string reason = "")
        {
            if (user.Id == Context.Client.CurrentUser.Id) return CustomResult.FromError($"Silly { Context.User.Mention}, I can't ban myself!");
            if (user.Id == Context.User.Id) return CustomResult.FromError($"{ Context.User.Mention}, you can't ban yourself");

            Embed e = new EmbedBuilder()
            {
                Title = "User Banned",
                Color = Color.Green,
                Description = $"{user.Mention} was banned from the server.",
                Fields = new List<EmbedFieldBuilder>()
                {
                    new EmbedFieldBuilder()
                    {
                        Name = "Duration",
                        Value = duration.ToString()
                    },
                    new EmbedFieldBuilder()
                    {
                        Name = "Reason",
                        Value = (reason.Length == 0) ? "No reason given." : reason
                    }
                }
            }.Build();
            await ReplyAsync(embed: e);
            return CustomResult.FromSuccess();
        }
        */

    }
}
