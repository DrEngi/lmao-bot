import urllib.request
import discord
import io
from PIL import Image, ImageDraw, ImageFont

async def get_avatar(mentioned):
    url = mentioned.avatar_url
    if url == "":
        url = mentioned.default_avatar_url
    req = urllib.request.Request(
        url,
        data=None,
        headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        }
    )
    f = urllib.request.urlopen(req)
    with io.open("img/pfp.png", "wb") as img:
        img.write(f.read())
    return Image.open("img/pfp.png")

def change_opacity(img, opacity): # Changes the opacity of Image object `img` to proportion out of 1 `opacity`
    img = img.convert("RGBA")
    pixel_data = img.getdata()

    new_pixel_data = []
    for pixel in pixel_data:
        new_pixel_data.append((pixel[0], pixel[1], pixel[2], round(opacity * 255)))

    img.putdata(new_pixel_data)
    return img

async def beautiful(mentioned):
    img = await get_avatar(mentioned)
    beautiful = Image.open("img/beautiful.png").convert('RGBA')

    canvas_w, canvas_h = beautiful.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen1 = img.resize((288,288)).convert('RGBA')
    specimen2 = img.resize((285,285)).convert('RGBA')

    canvas.paste(specimen1, (712, 76), specimen1)
    canvas.paste(specimen2, (712, 700), specimen2)
    canvas.paste(beautiful, (0,0), beautiful)
    canvas.save("img/beautiful_person.png")

async def ugly(mentioned):
    img = await get_avatar(mentioned)
    ugly = Image.open("img/ugly.png").convert('RGBA')

    canvas_w, canvas_h = ugly.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((100,100))

    canvas.paste(specimen, (158, 96), specimen.convert('RGBA'))
    canvas.paste(ugly, (0,0), ugly)
    canvas.save("img/ugly_person.png")

async def triggered(mentioned):
    img = await get_avatar(mentioned)
    triggered = Image.open("img/triggered.png").convert('RGBA')

    canvas_w, canvas_h = triggered.size
    specimen = img.resize((canvas_w, canvas_h)).convert('RGBA')

    specimen.paste(triggered.convert('RGBA'), (0,0), triggered)
    specimen.save("img/triggered_person.png")

async def victory(mentioned):
    img = await get_avatar(mentioned)
    victory = Image.open("img/victory.png").convert('RGBA')

    canvas_w, canvas_h = victory.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((333,333))

    canvas.paste(specimen, (353, 219), specimen.convert('RGBA'))
    canvas.paste(victory, (0,0), victory)
    canvas.save("img/victory_person.png")

async def wanted(mentioned):
    img = await get_avatar(mentioned)
    wanted = Image.open("img/wanted.png").convert('RGBA')

    specimen = img.resize((244,239))
    specimen = change_opacity(specimen, 0.5)

    wanted.paste(specimen, (76, 191), specimen.convert('RGBA'))
    wanted.save("img/wanted_person.png")

async def whos_that(mentioned):
    img = await get_avatar(mentioned)
    whos_that = Image.open("img/whos_that.png").convert('RGBA')

    canvas_w, canvas_h = whos_that.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    #specimen = img.resize((202,207)).convert('RGBA')
    specimen = img.resize((296,182)).convert('RGBA')

    #canvas.paste(specimen, (155, 454), specimen)
    canvas.paste(specimen, (23, 432), specimen)
    canvas.paste(whos_that, (0,0), whos_that)
    canvas.save("img/whos_that_person.png")

async def seen_from_above(mentioned):
    img = await get_avatar(mentioned)
    seen_from_above = Image.open("img/seen_from_above.png").convert('RGBA')

    canvas_w, canvas_h = seen_from_above.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((202,207)).convert('RGBA')

    canvas.paste(specimen, (155, 833), specimen)
    canvas.paste(seen_from_above, (0,0), seen_from_above)

    txt = Image.new('RGBA', canvas.size, (255,255,255,0))
    fnt = ImageFont.truetype('arial.ttf', 32)
    fill = (0,0,0,255)
    d = ImageDraw.Draw(txt)

    user_text = mentioned.name
    user_text_w, user_text_h = d.textsize(user_text, font=fnt)
    d.text((canvas_w/4 - user_text_w/2, canvas_h - user_text_h - 68), user_text, font=fnt, fill=fill)

    out = Image.alpha_composite(canvas, txt)
    out.save("img/seen_from_above_person.png")
