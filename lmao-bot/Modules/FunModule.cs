using Discord;
using Discord.Commands;
using lmao_bot.Services;
using lmao_bot.Utilities;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace lmao_bot.Modules
{
    public class FunModule: ModuleBase
    {
        private ImageService Image;

        public FunModule(ImageService image)
        {
            this.Image = image;
        }
        
        [Command("say")]
        [Alias("speak")]
        [Summary("Repeat after me")]
        public async Task Say([Remainder]string text)
        {
            await ReplyAsync(MessageUtil.CleanMention(text));
        }

        [Command("booty")]
        [Alias("butt")]
        [Summary("Sends a random SFW booty image in the chat")]
        public async Task Booty()
        {
            IDisposable typing = Context.Channel.EnterTypingState();
            await Context.Channel.SendFileAsync(Image.GetRandomBooty(), "booty.jpg");
            typing.Dispose();
        }

        [Command("moon")]
        [Alias("flash")]
        [Summary("Moons the selected member with a SFW booty image")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Moon(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            await Context.Channel.SendFileAsync(Image.GetRandomBooty(), "booty.jpg", user.Mention + ", you have been mooned by " + Context.Message.Author.Mention + "!");
            typing.Dispose();
        }

        [Command("deepfry")]
        [Summary("Deepfries an attached image, an image via URL, a mention user's profile picture, or one's own profile picture.")]
        public async Task<RuntimeResult> Deepfry(IGuildUser user = null, string url = null)
        {
            return CustomResult.FromError("Deepfry is not yet implemented");
        }

        [Command("beautiful")]
        [Summary("Lets a mentioned member know they're beautiful with a frame from gravity falls")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Beautiful(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetBeautifulImage(user);
            await Context.Channel.SendFileAsync(stream, "beautiful.jpg", user.Mention + " :heart:");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("ugly")]
        [Summary("Lets a mentioned member know that they're ugly with a frame from SpongeBob.")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Ugly(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetUglyImage(user);
            await Context.Channel.SendFileAsync(stream, "ugly.jpg", user.Mention + " :japanese_goblin:");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("garbage")]
        [Alias("trash")]
        [Summary("Lets a mentioned member know that they're garbage with a cute cartoon of a garbage can.")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Garbage(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetGarbageImage(user);
            await Context.Channel.SendFileAsync(stream, "garbage.jpg", user.Mention + " is GARBAGE! :wastebasket:");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("triggered")]
        [Summary("Warns people to stay away from a mentioned member; they're triggered!")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Triggered(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetTriggeredImage(user);
            await Context.Channel.SendFileAsync(stream, "triggered.jpg", user.Mention + " needs a safe space!");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("victory")]
        [Summary("Displays to everyone member's Victory Royale.")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Victory(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetVictoryImage(user);
            await Context.Channel.SendFileAsync(stream, "victory.jpg", user.Mention + " :trophy: Victory royale!");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("wanted")]
        [Summary("Puts member on a WANTED poster.")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task Wanted(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetWantedImage(user);
            await Context.Channel.SendFileAsync(stream, "wanted.jpg", user.Mention + " is WANTED!");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("whosthat")]
        [Summary("Who's that Pokémon? It's Pika-er... member?")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task WhosThat(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;

            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetWhosThatImage(user);
            await Context.Channel.SendFileAsync(stream, "whosthat.jpg", $"Who's that Pokémon?\n\nIt's... {user.Mention}!");
            await stream.DisposeAsync();
            typing.Dispose();
        }

        [Command("seenfromabove")]
        [Summary("Voltorb? Pokéball? Electrode? Nope. It's member, seen from above.")]
        [RequireContext(ContextType.Guild, ErrorMessage = "This command can only be run in a server.")]
        public async Task SeenFromAbove(IGuildUser user = null)
        {
            if (user == null) user = (IGuildUser)Context.User;
            
            IDisposable typing = Context.Channel.EnterTypingState();
            Stream stream = await Image.GetSeenFromAboveImage(user);
            await Context.Channel.SendFileAsync(stream, "seenfromabove.jpg", $"It's... {user.Mention}, seen from above!");
            await stream.DisposeAsync();
            typing.Dispose();
        }
    }
}
