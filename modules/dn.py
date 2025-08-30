# dn.py
from telethon import events
from bot_client import client
from PIL import Image, ImageSequence
import tempfile
import os

# Threshold for NSFW detection
SKIN_RATIO_THRESHOLD = 0.3

# Store DN state per chat
dn_enabled = {}

def detect_nudity(image_path):
    """Detects NSFW based on skin pixel ratio"""
    try:
        img = Image.open(image_path).convert("RGB")
    except:
        return False

    width, height = img.size
    pixels = img.load()
    skin_pixels = 0
    total_pixels = width * height

    for x in range(width):
        for y in range(height):
            r, g, b = pixels[x, y]
            if r > 95 and g > 40 and g < 100 and b > 20 and abs(r - g) > 15 and r > b:
                skin_pixels += 1

    skin_ratio = skin_pixels / total_pixels
    return skin_ratio > SKIN_RATIO_THRESHOLD

def detect_nudity_gif(image_path):
    """Check all frames in GIF"""
    try:
        img = Image.open(image_path)
    except:
        return False

    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGB")
        width, height = frame.size
        pixels = frame.load()
        skin_pixels = 0
        total_pixels = width * height
        for x in range(width):
            for y in range(height):
                r, g, b = pixels[x, y]
                if r > 95 and g > 40 and g < 100 and b > 20 and abs(r - g) > 15 and r > b:
                    skin_pixels += 1
        skin_ratio = skin_pixels / total_pixels
        if skin_ratio > SKIN_RATIO_THRESHOLD:
            return True
    return False

# Command to turn DN on/off
@client.on(events.NewMessage(pattern=r'^/dn (on|off)$'))
async def dn_toggle(event):
    chat_id = event.chat_id
    state = event.pattern_match.group(1)
    if state == "on":
        dn_enabled[chat_id] = True
        await event.reply("✅ Auto NSFW deletion is ON for this chat.")
    else:
        dn_enabled[chat_id] = False
        await event.reply("❌ Auto NSFW deletion is OFF for this chat.")

# Monitor new messages
@client.on(events.NewMessage)
async def check_media(event):
    chat_id = event.chat_id
    if not dn_enabled.get(chat_id, False):
        return
    if not event.media:
        return

    # Download media to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    await event.download_media(temp_file.name)

    is_nsfw = False
    if temp_file.name.lower().endswith((".gif", ".webp")):  # GIF or sticker
        is_nsfw = detect_nudity_gif(temp_file.name)
    else:  # Regular image
        is_nsfw = detect_nudity(temp_file.name)

    if is_nsfw:
        try:
            await event.delete()
            await event.respond("⚠️ NSFW content detected and deleted.")
        except:
            pass

    os.unlink(temp_file.name)
