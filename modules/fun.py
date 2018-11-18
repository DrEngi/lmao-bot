import urllib.request
import discord
from discord.ext import commands
from utils import usage, deeppyer, perms
import io
import os
import re
import random
from PIL import Image, ImageDraw, ImageFont

def save_url(url, path):
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    fi = urllib.request.urlopen(req)
    with io.open(path, "wb") as fo:
        fo.write(fi.read())
    return path

async def save_file_from_ctx(ctx, path, detect_ext=False):
    files = ctx.message.attachments
    ext = ""
    if len(files) > 0:
        if detect_ext:
            ext = os.path.splitext(files[0].filename)[1]
        await files[0].save(f"{path}{ext}")
        return f"{path}{ext}"
    command = ctx.invoked_with
    msg_no_prefix = ctx.message.content[ctx.message.content.find(command):]
    url = msg_no_prefix[len(command) + 1:].strip()
    try:
        if detect_ext:
            ext = os.path.splitext(url)[1]
        return save_url(url, f"{path}{ext}")
    except (ValueError, urllib.error.HTTPError) as e:
        if detect_ext:
            ext = ".png"
        if len(ctx.message.mentions) > 0:
            return save_url(ctx.message.mentions[0].avatar_url, f"{path}{ext}")
        else:
            return save_url(ctx.author.avatar_url, f"{path}{ext}")

def get_image_from_url(url, path):
    return Image.open(save_url(url, path))

def get_avatar(mentioned):
    return get_image_from_url(mentioned.avatar_url, "img/pfp.png")



def change_opacity(img, opacity): # Changes the opacity of Image object `img` to proportion out of 1 `opacity`
    img = img.convert("RGBA")
    pixel_data = img.getdata()

    new_pixel_data = []
    for pixel in pixel_data:
        new_pixel_data.append((pixel[0], pixel[1], pixel[2], round(opacity * 255)))

    img.putdata(new_pixel_data)
    return img

async def beautiful(mentioned):
    img = get_avatar(mentioned)
    beautiful = Image.open("img/beautiful.png").convert('RGBA')

    canvas_w, canvas_h = beautiful.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen1 = img.resize((288,288)).convert('RGBA')
    specimen2 = img.resize((285,285)).convert('RGBA')

    canvas.paste(specimen1, (712, 76), specimen1)
    canvas.paste(specimen2, (712, 700), specimen2)
    canvas.paste(beautiful, (0,0), beautiful)
    canvas.save(f"img/beautiful_{mentioned.id}.png")

async def ugly(mentioned):
    img = get_avatar(mentioned)
    ugly = Image.open("img/ugly.png").convert('RGBA')

    canvas_w, canvas_h = ugly.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((100,100))

    canvas.paste(specimen, (158, 96), specimen.convert('RGBA'))
    canvas.paste(ugly, (0,0), ugly)
    canvas.save(f"img/ugly_{mentioned.id}.png")

async def garbage(mentioned):
    img = get_avatar(mentioned)
    garbage = Image.open("img/garbage.png")

    canvas_w, canvas_h = garbage.size
    canvas = Image.open("img/garbage_orig.png").resize((canvas_w, canvas_h)).convert("RGBA")

    specimen = img.resize((202,202))

    canvas.paste(specimen, (197, 118), specimen.convert("RGBA"))
    canvas.paste(garbage, (0, 0), garbage.convert("RGBA"))
    canvas.save(f"img/garbage_{mentioned.id}.png")

async def triggered(mentioned):
    img = get_avatar(mentioned)
    triggered = Image.open("img/triggered.png").convert('RGBA')

    canvas_w, canvas_h = triggered.size
    specimen = img.resize((canvas_w, canvas_h)).convert('RGBA')

    specimen.paste(triggered.convert('RGBA'), (0,0), triggered)
    specimen.save(f"img/triggered_{mentioned.id}.png")

async def victory(mentioned):
    img = get_avatar(mentioned)
    victory = Image.open("img/victory.png").convert('RGBA')

    canvas_w, canvas_h = victory.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((333,333))

    canvas.paste(specimen, (353, 219), specimen.convert('RGBA'))
    canvas.paste(victory, (0,0), victory)
    canvas.save(f"img/victory_{mentioned.id}.png")

async def wanted(mentioned):
    img = get_avatar(mentioned)
    wanted = Image.open("img/wanted.png").convert('RGBA')

    specimen = img.resize((244,239))
    specimen = change_opacity(specimen, 0.5)

    wanted.paste(specimen, (76, 191), specimen.convert('RGBA'))
    wanted.save(f"img/wanted_{mentioned.id}.png")

async def whos_that(mentioned):
    img = get_avatar(mentioned)
    whos_that = Image.open("img/whos_that.png").convert('RGBA')

    canvas_w, canvas_h = whos_that.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    #specimen = img.resize((202,207)).convert('RGBA')
    specimen = img.resize((296,182)).convert('RGBA')

    #canvas.paste(specimen, (155, 454), specimen)
    canvas.paste(specimen, (23, 432), specimen)
    canvas.paste(whos_that, (0,0), whos_that)
    canvas.save(f"img/whos_that_{mentioned.id}.png")

async def seen_from_above(mentioned):
    img = get_avatar(mentioned)
    seen_from_above = Image.open("img/seen_from_above.png").convert('RGBA')

    canvas_w, canvas_h = seen_from_above.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((202,207)).convert('RGBA')

    canvas.paste(specimen, (155, 833), specimen)
    canvas.paste(seen_from_above, (0,0), seen_from_above)

    txt = Image.new('RGBA', canvas.size, (255,255,255,0))
    fnt = ImageFont.truetype('fonts/arial.ttf', 32)
    fill = (0,0,0,255)
    d = ImageDraw.Draw(txt)

    user_text = mentioned.name
    user_text_w, user_text_h = d.textsize(user_text, font=fnt)
    d.text((canvas_w/4 - user_text_w/2, canvas_h - user_text_h - 68), user_text, font=fnt, fill=fill)

    out = Image.alpha_composite(canvas, txt)
    out.save(f"img/seen_from_above_{mentioned.id}.png")

async def beautiful_welcome(member, channel, mention=True):
    await beautiful(member)
    img_file = "img/beautiful_{}.png".format(member.id)
    user = member
    if mention:
        user = member.mention
    await channel.send(f"Welcome to {member.guild.name}, {user}!", file=discord.File(img_file))
    os.remove(img_file)

class Fun:

    __slots__ = ('bot')

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="say", aliases=["speak", "repeat"])
    async def cmd_say(self, ctx, *, arg=""):    # Allows user to have lmao-bot say a message
        if arg == "":
            await ctx.send(f"You have to have a message for me to say. e.g. `{ctx.prefix}say Replacing asses by day, kicking asses by night.`")
        else:
            try:
                await ctx.message.delete()
            except discord.errors.Forbidden:
                pass
            except discord.errors.NotFound:
                pass
            if perms.get_perms(ctx.message).mention_everyone:
                await ctx.send(arg)
            else:
                await ctx.send(re.sub(r"@(everyone|here)", "@\u200b\\1", arg))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="booty", aliases=["butt"])
    async def cmd_booty(self, ctx):  # Sends a random SFW booty pic in the channel
        await ctx.send(file=discord.File("img/booties/booty" + str(random.randint(1,10)) + ".jpg"))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="moon", aliases=["flash"])
    async def cmd_moon(self, ctx, *, arg=""):   # Allows users to moon other users with SFW booty pics
        mentioned = ""
        for mentioned_user in ctx.message.raw_mentions:
            mentioned += "<@" + str(mentioned_user) + "> "
        if mentioned != "":
            mentioned = mentioned[:-1]
            mention_msg = f"{mentioned}, you have been mooned by {ctx.author.mention}!"
        else:
            mention_msg = ""
        await ctx.send(mention_msg, file=discord.File("img/booties/booty" + str(random.randint(1,10)) + ".jpg"))
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="deepfry")
    async def cmd_deepfry(self, ctx):
        await ctx.trigger_typing()
        fp = await save_file_from_ctx(ctx, f"img/deepfry_{ctx.message.id}.jpg")
        try:
            img = Image.open(fp)
        except OSError:
            img = get_avatar(ctx.author)
        fried = await deeppyer.deepfry(img)
        fried.save(fp)
        await ctx.send(file=discord.File(fp))
        os.remove(fp)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="beautiful")
    async def cmd_beautiful(self, ctx):
        await ctx.trigger_typing()
        try:
            beautiful_person = ctx.message.mentions[0]
        except IndexError:
            beautiful_person = ctx.author
        await beautiful(beautiful_person)
        img_file = "img/beautiful_{}.png".format(beautiful_person.id)
        await ctx.send(f"{beautiful_person.mention} :heart:", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="ugly")
    async def cmd_ugly(self, ctx):
        await ctx.trigger_typing()
        try:
            ugly_person = ctx.message.mentions[0]
        except IndexError:
            ugly_person = ctx.author
        await ugly(ugly_person)
        img_file = f"img/ugly_{ugly_person.id}.png"
        await ctx.send(f"{ugly_person.mention} :japanese_goblin:", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="garbage", aliases=["trash"])
    async def cmd_garbage(self, ctx):
        await ctx.trigger_typing()
        try:
            garbage_person = ctx.message.mentions[0]
        except IndexError:
            garbage_person = ctx.author
        await garbage(garbage_person)
        img_file = f"img/garbage_{garbage_person.id}.png"
        await ctx.send(f"{garbage_person.mention} is GARBAGE! :wastebasket:", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="triggered")
    async def cmd_triggered(self, ctx):
        await ctx.trigger_typing()
        try:
            triggered_person = ctx.message.mentions[0]
        except IndexError:
            triggered_person = ctx.author
        await triggered(triggered_person)
        img_file = f"img/triggered_{triggered_person.id}.png"
        await ctx.send(f"{triggered_person.mention} needs a safe space!", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="victory")
    async def cmd_victory(self, ctx):
        await ctx.trigger_typing()
        try:
            victory_person = ctx.message.mentions[0]
        except IndexError:
            victory_person = ctx.author
        await victory(victory_person)
        img_file = f"img/victory_{victory_person.id}.png"
        await ctx.send(f"{victory_person.mention} :trophy: Victory Royale!", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="wanted")
    async def cmd_wanted(self, ctx):
        await ctx.trigger_typing()
        try:
            wanted_person = ctx.message.mentions[0]
        except IndexError:
            wanted_person = ctx.author
        await wanted(wanted_person)
        img_file = f"img/wanted_{wanted_person.id}.png"
        await ctx.send(f"{wanted_person.mention} is WANTED!", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="whosthat")
    async def cmd_whos_that(self, ctx):
        await ctx.trigger_typing()
        try:
            whos_that_person = ctx.message.mentions[0]
        except IndexError:
            whos_that_person = ctx.author
        await whos_that(whos_that_person)
        img_file = f"img/whos_that_{whos_that_person.id}.png"
        await ctx.send(f"Who's that Pokémon?\n\nIt's... {whos_that_person.mention}!", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

    @commands.command(name="seenfromabove")
    async def cmd_seen_from_above(self, ctx):
        await ctx.trigger_typing()
        try:
            seen_from_above_person = ctx.message.mentions[0]
        except IndexError:
            seen_from_above_person = ctx.author
        await seen_from_above(seen_from_above_person)
        img_file = f"img/seen_from_above_{seen_from_above_person.id}.png"
        await ctx.send(f"It's... {seen_from_above_person.mention}, seen from above!", file=discord.File(img_file))
        os.remove(img_file)
        usage.update(ctx)
        return ctx.command.name

def setup(bot):
    bot.add_cog(Fun(bot))
