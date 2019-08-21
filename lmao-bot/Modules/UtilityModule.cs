using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using UrbanDictionnet;

namespace lmao_bot.Modules
{
    public class UtilityModule : ModuleBase
    {
        UrbanDictionaryService UDService;

        public UtilityModule(UrbanDictionaryService udservice)
        {
            UDService = udservice;
        }

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
            IDisposable typing = Context.Channel.EnterTypingState();
            SocketGuildUser guildUser = (SocketGuildUser)Context.User;
            ChannelPermissions permissions = guildUser.GetPermissions((IGuildChannel)Context.Channel);
            IReadOnlyCollection<IUser> users = await Context.Channel.GetUsersAsync().ElementAt(0);

            Random random = new Random();
            int r = random.Next(users.Count);

            if (permissions.MentionEveryone) await ReplyAsync(users.ElementAt(r).Mention + " " + text);
            else await ReplyAsync(Utilities.MessageUtil.CleanMention(users.ElementAt(r).Mention + " " + text));
            typing.Dispose();
        }

        [Command("urban")]
        [Alias("define", "dictionary", "urbandictionary", "ud")]
        [RequireNsfw(ErrorMessage = "Whoa-ho-ho-ho, hold your horses. The Urban Dictionary command only works in NSFW channels.")]
        public async Task Urban([Remainder]string word)
        {
            IDisposable typing = Context.Channel.EnterTypingState();
            WordDefine definition = await UDService.Define(word);

            Embed e = new EmbedBuilder()
            {
                Title = $"Urban Dictionary Entry for {definition.Definitions[0].Word}",
                Description = definition.Definitions[0].Definition,
                Fields = new List<EmbedFieldBuilder>()
                {
                    new EmbedFieldBuilder()
                    {
                        Name = "Example",
                        Value = definition.Definitions[0].Example
                    }
                },
                Color = Color.Orange,
                Footer = new EmbedFooterBuilder()
                {
                    Text = $"Definition ID: {definition.Definitions[0].DefId}"
                }
            }.Build();
            await ReplyAsync(embed: e);

            typing.Dispose();
        }
    }
}