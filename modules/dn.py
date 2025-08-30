from telethon import events
from bot_client import client
import json
import os
import aiohttp

# JSON file to store dn settings
DN_FILE = "dn.json"

if not os.path.exists(DN_FILE):
    with open(DN_FILE, "w") as f:
        json.dump({}, f)

def load_dn():
    with open(DN_FILE, "r") as f:
        return json.load(f)

def save_dn(data):
    with open(DN_FILE, "w") as f:
        json.dump(data, f)

dn_data = load_dn()

# Command: /dn on/off
@client.on(events.NewMessage(pattern=r'/dn (on|off)'))
async def dn_command(event):
    chat = await event.get_chat()
    arg = event.pattern_match.group(1).lower()

    if arg == "on":
        dn_data[str(chat.id)] = True
        save_dn(dn_data)
        await event.reply("✅ NSFW detection is now ON for this chat.")
    else:
        dn_data[str(chat.id)] = False
        save_dn(dn_data)
        await event.reply("❌ NSFW detection is now OFF for this chat.")

# Function to check NSFW via free API
async def is_nsfw(file_path):
    url = "https://api.deepai.org/api/nsfw-detector"
    api_key = "quickstart-QUdJIGlzIGNvbWluZy4uLi4K"  # Free quickstart key
    async with aiohttp.ClientSession() as session:
        with open(file_path, "rb") as f:
            data = {'image': f}
            headers = {'api-key': api_key}
            async with session.post(url, data=data, headers=headers) as resp:
                result = await resp.json()
                nsfw_score = result.get("output", {}).get("nsfw_score", 0)
                return nsfw_score > 0.5  # Adjust threshold if needed

# Watch messages
@client.on(events.NewMessage())
async def detect_nsfw(event):
    chat_id = str(event.chat_id)
    if not dn_data.get(chat_id):
        return  # Detection off

    if event.photo or event.media:
        # Download file temporarily
        file_path = await event.download_media()
        if file_path:
            if await is_nsfw(file_path):
                await event.delete()
                await event.respond("⚠️ NSFW content detected and deleted!")
            os.remove(file_path)
