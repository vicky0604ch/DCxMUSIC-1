/eval import os
import re
import random

import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance
from PIL import ImageFilter, ImageFont, ImageOps

from unidecode import unidecode
from youtubesearchpython.future import VideosSearch

from DCxMUSIC import app
from config import YOUTUBE_IMG_URL

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()

async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        # Futuristic view
        colors = ["#3498db", "#f1c40f", "#2ecc71", "#e74c3c", "#9b59b6"]
        border = random.choice(colors)
        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        bg_bright = ImageEnhance.Brightness(image1)
        bg_logo = bg_bright.enhance(1.1)
        bg_contra = ImageEnhance.Contrast(bg_logo)
        bg_logo = bg_contra.enhance(1.1)
        logox = ImageOps.expand(bg_logo, border=7, fill=f"{border}")
        background = changeImageSize(1280, 720, logox)

        # Add futuristic effects
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype("DCxMUSIC/assets/font.ttf", 30)
        draw.text((10, 10), unidecode(app.name), fill="#ffffff", font=font)
        draw.text((10, 50), clear(title), fill="#ffffff", font=font)
        draw.text((10, 90), f"{channel} | {views[:23]}", fill="#ffffff", font=font)
        draw.text((10, 130), f"{duration[:23]}", fill="#ffffff", font=font)

        # Add futuristic shapes
        draw.polygon([(1280 - 10, 10), (1280 - 10, 50), (1280 - 50, 30)], fill="#ffffff")
        draw.ellipse([(1280 - 50, 10), (1280 - 10, 50)], outline="#ffffff", fill="#ffffff")

        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        background.save(f"cache/{videoid}.png")
        return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
