from PIL import Image, ImageOps, ImageEnhance
from enum import Enum
import aiohttp, asyncio, math, argparse

class DeepfryTypes(Enum):
    """
    Enum for the various possible effects added to the image.
    """
    RED = 1
    BLUE = 2

class Colours:
    RED = (254, 0, 2)
    YELLOW = (255, 255, 15)
    BLUE = (36, 113, 229)
    WHITE = (255,) * 3

async def deepfry(img: Image, *, url_base: str='westcentralus', session: aiohttp.ClientSession=None, type=DeepfryTypes.RED) -> Image:
    """
    Deepfry an image.

    img: PIL.Image - Image to deepfry.
    [token]: str - Token to use for Microsoft facial recognition API. If this is not supplied, lens flares will not be added.
    [url_base]: str = 'westcentralus' - API base to use. Only needed if your key's region is not `westcentralus`.
    [session]: aiohttp.ClientSession - Optional session to use with API requests. If provided, may provide a bit more speed.

    Returns: PIL.Image - Deepfried image.
    """
    img = img.copy().convert('RGB')

    if type not in DeepfryTypes:
        raise ValueError(f'Unknown deepfry type "{type}", expected a value from deeppyer.DeepfryTypes')

    # Crush image to hell and back
    img = img.convert('RGB')
    width, height = img.width, img.height
    img = img.resize((int(width ** .75), int(height ** .75)), resample=Image.LANCZOS)
    img = img.resize((int(width ** .88), int(height ** .88)), resample=Image.BILINEAR)
    img = img.resize((int(width ** .9), int(height ** .9)), resample=Image.BICUBIC)
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, 4)

    # Generate red and yellow overlay for classic deepfry effect
    r = img.split()[0]
    r = ImageEnhance.Contrast(r).enhance(2.0)
    r = ImageEnhance.Brightness(r).enhance(1.5)

    if type == DeepfryTypes.RED:
        r = ImageOps.colorize(r, Colours.RED, Colours.YELLOW)
    elif type == DeepfryTypes.BLUE:
        r = ImageOps.colorize(r, Colours.BLUE, Colours.WHITE)

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, r, 0.75)
    img = ImageEnhance.Sharpness(img).enhance(100.0)

    return img

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Deepfry an image, optionally adding lens flares for eyes.')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0', help='Display program version.')
    parser.add_argument('-t', '--token', help='Token to use for facial recognition API.')
    parser.add_argument('-o', '--output', help='Filename to output to.')
    parser.add_argument('file', metavar='FILE', help='File to deepfry.')
    args = parser.parse_args()

    token = args.token
    img = Image.open(args.file)
    out = args.output or './deepfried.jpg'

    loop = asyncio.get_event_loop()
    img = loop.run_until_complete(deepfry(img, token=token))

    img.save(out, 'jpeg')
