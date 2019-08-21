using Discord;
using Discord.Commands;
using Discord.WebSocket;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class UtilityModule : ModuleBase
    {
        [Command("avatar")]
        [Alias("pfp", "image", "profilepic", "profilepicture")]
        public async Task Avatar(string user = "")
        {
            IDisposable typing = Context.Channel.EnterTypingState();
            if (Context.Message.MentionedUserIds.Count <= 0) await ReplyAsync(Context.User.GetAvatarUrl());
            else
            {
                IGuildUser userClass = await Context.Guild.GetUserAsync(Context.Message.MentionedUserIds.ElementAt(0));
                await ReplyAsync(userClass.GetAvatarUrl());
            }
            typing.Dispose();
        }

        [Command("someone")]
        [Alias("@someone", "@random", "mention")]
        public async Task Someone([Remainder]string text)
        {
            SocketGuildUser guildUser = (SocketGuildUser)Context.User;
            ChannelPermissions permissions = guildUser.GetPermissions((IGuildChannel)Context.Channel);
            IReadOnlyCollection<IUser> users = await Context.Channel.GetUsersAsync().ElementAt(0);

            Random random = new Random();
            int r = random.Next(users.Count);

            if (permissions.MentionEveryone) await ReplyAsync(users.ElementAt(r).Mention + " " + text);
            else await ReplyAsync(Utilities.MessageUtil.CleanMention(users.ElementAt(r).Mention + " " + text));
        }   
    }
}