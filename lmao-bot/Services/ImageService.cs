using Discord;
using System;
using System.Collections.Generic;
using System.IO;
using System.Text;
using System.Threading.Tasks;
using Flurl.Http;
using SixLabors.ImageSharp.Processing;
using SixLabors.ImageSharp.Formats.Jpeg;
using SixLabors.ImageSharp;
using SixLabors.ImageSharp.PixelFormats;
using SixLabors.ImageSharp.Formats;
using SixLabors.Fonts;

namespace lmao_bot.Services
{
    public class ImageService
    {
        private string ImageLocation = "img/";
        private string WhiteCanvas = "img/white_canvas.png";

        FontCollection Fonts;
        FontFamily Arial;

        public ImageService()
        {
            Fonts = new FontCollection();
            Arial = Fonts.Install("fonts/arial.ttf");
        }

        public Stream GetRandomBooty()
        {
            Random rand = new Random();
            string bootyFileName = "booty" + rand.Next(11) + ".jpg";
            string path = ImageLocation + "booties/" + bootyFileName;

            if (!File.Exists(path)) return null;
            else
            {
                return File.OpenRead(path);
            }
        }

        private async Task<Image<Rgba32>> GetUserAvatar(IGuildUser user)
        {
            if (String.IsNullOrEmpty(user.GetAvatarUrl())) return SixLabors.ImageSharp.Image.Load<Rgba32>(await user.GetDefaultAvatarUrl().GetBytesAsync());
            else return SixLabors.ImageSharp.Image.Load<Rgba32>(await user.GetAvatarUrl().GetBytesAsync());
        }

        public async Task<Stream> GetBeautifulImage(IGuildUser user)
        {
            string path = ImageLocation + "beautiful.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image beautifulTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(beautifulTemplate.Width, beautifulTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen1 = avatarImage.Clone(x => x.Resize(288, 288)))
                using (SixLabors.ImageSharp.Image specimen2 = avatarImage.Clone(x => x.Resize(285, 285)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen1, location: new SixLabors.Primitives.Point(712, 76), 1));
                    whiteCanvas.Mutate(x => x.DrawImage(specimen2, location: new SixLabors.Primitives.Point(712, 700), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(beautifulTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));
                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetUglyImage(IGuildUser user)
        {
            string path = ImageLocation + "ugly.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image uglyTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(uglyTemplate.Width, uglyTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(100, 100)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(158, 96), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(uglyTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));
                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetGarbageImage(IGuildUser user)
        {
            string path = ImageLocation + "garbage.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image garbageTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(garbageTemplate.Width, garbageTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(202, 202)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(197, 118), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(garbageTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));
                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetTriggeredImage(IGuildUser user)
        {
            string path = ImageLocation + "triggered.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image triggeredTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(triggeredTemplate.Width, triggeredTemplate.Height)))
                {
                    triggeredTemplate.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(0, 0), 0.5f));
                }

                triggeredTemplate.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetVictoryImage(IGuildUser user)
        {
            string path = ImageLocation + "victory.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image victoryTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(victoryTemplate.Width, victoryTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(333, 333)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(353, 219), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(victoryTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));
                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetWantedImage(IGuildUser user)
        {
            string path = ImageLocation + "wanted.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image triggeredTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(244, 239)))
                {
                    triggeredTemplate.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(76, 191), 1));
                }

                triggeredTemplate.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetWhosThatImage(IGuildUser user)
        {
            string path = ImageLocation + "whos_that.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image victoryTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(victoryTemplate.Width, victoryTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(296, 182)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(23, 432), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(victoryTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));
                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }

        public async Task<Stream> GetSeenFromAboveImage(IGuildUser user)
        {
            string path = ImageLocation + "seen_from_above.png";
            string avatarURL = user.GetAvatarUrl();
            Stream stream = new MemoryStream();

            using (SixLabors.ImageSharp.Image avatarImage = await GetUserAvatar(user))
            using (SixLabors.ImageSharp.Image whiteCanvas = SixLabors.ImageSharp.Image.Load<Rgba32>(WhiteCanvas))
            using (SixLabors.ImageSharp.Image seenFromAboveTemplate = SixLabors.ImageSharp.Image.Load<Rgba32>(path))
            {
                whiteCanvas.Mutate(x => x.Resize(seenFromAboveTemplate.Width, seenFromAboveTemplate.Height));

                using (SixLabors.ImageSharp.Image specimen = avatarImage.Clone(x => x.Resize(202, 207)))
                {
                    whiteCanvas.Mutate(x => x.DrawImage(specimen, location: new SixLabors.Primitives.Point(155, 833), 1));
                }

                whiteCanvas.Mutate(x => x.DrawImage(seenFromAboveTemplate, location: new SixLabors.Primitives.Point(0, 0), 1));

                string text = user.Nickname == null ? user.Username : user.Nickname;
                
                Font font = Arial.CreateFont(32f);
                

                var measure = TextMeasurer.Measure(text, new RendererOptions(font));

                whiteCanvas.Mutate(x => x.DrawText(
                    text,
                    font,
                    SixLabors.ImageSharp.Color.Black,
                    new SixLabors.Primitives.PointF(whiteCanvas.Width / 4 - measure.Width / 2, whiteCanvas.Height - measure.Height - 68)));

                whiteCanvas.SaveAsJpeg(stream);
                stream.Position = 0;
                return stream;
            }
        }
    }
}
