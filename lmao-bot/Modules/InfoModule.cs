using Discord;
using Discord.Commands;
using Discord.WebSocket;
using lmao_bot.Models.ServerSettings;
using lmao_bot.Services;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class InfoModule : ModuleBase
    {
        private DatabaseService Database;
        private DiscordShardedClient Client;

        public InfoModule(DatabaseService service, DiscordShardedClient client)
        {
            Database = service;
            Client = client;
        }

        [Command("prefix")]
        [Summary("Change the bot prefix for this server")]
        [RequireBotDeveloper(Group = "Group")]
        [RequireUserPermission(GuildPermission.ManageMessages, Group = "Group")]
        [RequireContext(ContextType.Guild)]
        public async Task Prefix(string prefix = null)
        {
            if (prefix == null)
            {
                var embed = new EmbedBuilder()
                {
                    Title = "Prefix Settings",
                    Description = $"Current Prefix: **{await Database.GetPrefix((long)Context.Guild.Id)}**",
                    Color = Color.Orange,
                    Footer = new EmbedFooterBuilder()
                    {
                        Text = "Include your new prefix as an argument if you want to change it"
                    }
                }.Build();
                await ReplyAsync(embed: embed);
            }
            else
            {
                LmaoBotServer settings = await Database.GetServerSettings().GetServerSettings((long)Context.Guild.Id);
                string oldPrefix = settings.BotSettings.CommandPrefix;
                settings.BotSettings.CommandPrefix = prefix;

                await Database.GetServerSettings().SetServerPrefix((long)Context.Guild.Id, prefix);
                Database.SetPrefix((long)Context.Guild.Id, prefix);

                var embed = new EmbedBuilder()
                {
                    Title = "Prefix Settings Changed",
                    Description = $"Old Prefix: {oldPrefix}\n**New Prefix: {prefix}**",
                    Color = Color.Orange,
                    Footer = new EmbedFooterBuilder()
                }.Build();
                await ReplyAsync(embed: embed);
            }
        }

        [Command("info")]
        [Alias("about", "botinfo")]
        [Summary("Gives a brief description about the bot, including an invite to the support server.")]
        public async Task Info()
        {
            string desc = "I am a fun utility bot created by Firestar493#6963 and DrEngineer#8214 with discord.py in June 2018. I replace people's asses after they \"lmao\" or \"lmfao\". Try it out!\n " +
                          "I do all sorts of other things too, such as play music, provide moderation commands, and give answers from the almighty magic 8 - ball. Invite me to one of your servers to see for yourself!";

            var embed = new EmbedBuilder
            {
                Title = "Hello from lmao-bot! :wave:",
                ThumbnailUrl = Context.Client.CurrentUser.GetAvatarUrl(),
                Color = Color.Orange,
                Description = desc,
                Fields = new List<EmbedFieldBuilder>()
                {
                    new EmbedFieldBuilder()
                    {
                        Name = "Total Servers",
                        Value = Client.Guilds.Count,
                        IsInline = true
                    },
                    new EmbedFieldBuilder()
                    {
                        Name = "Shard Count",
                        Value = (await Context.Client.GetRecommendedShardCountAsync()),
                        IsInline = true
                    },
                    new EmbedFieldBuilder()
                    {
                         Name = "Invite me to your server",
                         Value = "[You won't regret it :eyes:](https://discordapp.com/oauth2/authorize?client_id=459432854821142529&scope=bot&permissions=336063575)",
                         IsInline = false
                    },
                    new EmbedFieldBuilder()
                    {
                        Name = "Join the support server",
                        Value = "[Send help pls](https://discord.gg/JQgB7p7)",
                        IsInline = false
                    },
                    new EmbedFieldBuilder()
                    {
                        Name = "Vote for me on DBL",
                        Value = "[The power is in your hands](https://discordbots.org/bot/459432854821142529/vote)",
                        IsInline = false
                    }
                },
                Footer = new EmbedFooterBuilder
                {
                    Text = "Try saying \"lmao help\" in a server I'm in!"
                }
            }.Build();
            await ReplyAsync(embed: embed);
        }

        [Command("support")]
        [Summary("Sends an invite link to the lmao-bot support server.")]
        public async Task Support()
        {
            await ReplyAsync("Need help with the bot? Don't worry, we've got your ass covered. Join the support server.\n\nhttps://discord.gg/JQgB7p7");
        }

        [Command("vote")]
        [Summary("Like lmao-bot? This gives you a link to vote for it on Discord Bot List!")]
        public async Task Vote()
        {
            var embed = new EmbedBuilder()
            {
                Title = "Vote for lmao-bot!",
                Description = "Like lmao-bot?\n\n[**Vote** for lmao-bot on Discord Bot List!](https://discordbots.org/bot/459432854821142529/vote)",
                ThumbnailUrl = Context.Client.CurrentUser.GetAvatarUrl(),
                Color = Color.Orange
            }.Build();
            await ReplyAsync(embed: embed);
        }

        [Command("invite")]
        [Summary("Need ass insurance in other servers? Invite lmao-bot to other servers you're in!")]
        public async Task Invite()
        {
            var embed = new EmbedBuilder()
            {
                Title = "Invite lmao-bot!",
                Description = "Need ass insurance in other servers you're in?\n\n[Click here to invite to more servers!](https://discordapp.com/oauth2/authorize?client_id=459432854821142529&scope=bot&permissions=336063575)",
                ThumbnailUrl = Context.Client.CurrentUser.GetAvatarUrl(),
                Color = Color.Orange
            }.Build();
            await ReplyAsync(embed: embed);
        }
    }
}