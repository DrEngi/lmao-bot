import urllib.request
import discord
import io
from PIL import Image

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

async def beautiful(mentioned):
    img = await get_avatar(mentioned)
    beautiful = Image.open("img/beautiful.png")

    canvas_w, canvas_h = beautiful.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen1 = img.resize((288,288))
    specimen2 = img.resize((285,285))

    canvas.paste(specimen1, (712, 76), specimen1.convert('RGBA'))
    canvas.paste(specimen2, (712, 700), specimen2.convert('RGBA'))
    canvas.paste(beautiful, (0,0), beautiful.convert('RGBA'))
    canvas.save("img/beautiful_person.png")

async def ugly(mentioned):
    img = await get_avatar(mentioned)
    ugly = Image.open("img/ugly.png")

    canvas_w, canvas_h = ugly.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((100,100))

    canvas.paste(specimen, (158, 96), specimen.convert('RGBA'))
    canvas.paste(ugly, (0,0), ugly.convert('RGBA'))
    canvas.save("img/ugly_person.png")

async def triggered(mentioned):
    img = await get_avatar(mentioned)
    triggered = Image.open("img/triggered.png")

    canvas_w, canvas_h = triggered.size
    specimen = img.resize((canvas_w, canvas_h)).convert('RGBA')

    specimen.paste(triggered.convert('RGBA'), (0,0), triggered.convert('RGBA'))
    specimen.save("img/triggered_person.png")

async def victory(mentioned):
    img = await get_avatar(mentioned)
    victory = Image.open("img/victory.png")

    canvas_w, canvas_h = victory.size
    canvas = Image.open("img/white_canvas.png").resize((canvas_w, canvas_h)).convert('RGBA')

    specimen = img.resize((333,333))

    canvas.paste(specimen, (353, 219), specimen.convert('RGBA'))
    canvas.paste(victory, (0,0), victory.convert('RGBA'))
    canvas.save("img/victory_person.png")
