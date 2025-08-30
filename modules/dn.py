from telethon import events
from bot_client import client
import json
import os

DN_FILE = "modules/dn.json"

# Load or create JSON file
if not os.path.exists(DN_FILE):
    with open(DN_FILE, "w") as f:
        json.dump({}, f)

with open(DN_FILE, "r") as f:
    dn_data = json.load(f)

# Helper to save JSON
def save_dn():
    with open(DN_FILE, "w") as f:
        json.dump(dn_data, f, indent=2)

# /dn command to toggle nudity deletion
@client.on(events.NewMessage(pattern=r'^/dn\s+(on|off)$'))
async def dn_toggle(event):
    chat = await event.get_chat()
    user = await event.get_sender()
    arg = event.pattern_match.group(1).lower()

    # Only admins can toggle
    try:
        participant = await client.get_permissions(chat, user.id)
        if not participant.is_admin:
            await event.reply("❌ Only admins can toggle nudity detection.")
            return
    except:
        await event.reply("❌ Cannot check admin status.")
        return

    dn_data[str(chat.id)] = arg == "on"
    save_dn()
    status = "enabled ✅" if arg == "on" else "disabled ❌"
    await event.reply(f"Automatic nudity deletion is now **{status}** in this chat.")

# Listen to all messages for nudity
@client.on(events.NewMessage())
async def dn_handler(event):
    chat_id = str(event.chat_id)
    if not dn_data.get(chat_id):
        return  # DN is off

    # Only process media messages
    if not event.media:
        return

    try:
        # Download media temporarily
        file_path = await event.download_media("/tmp/")
        from nudenet import NudeDetector
        detector = NudeDetector()
        result = detector.detect(file_path)

        # Check if the image is NSFW
        if result and result[0]["unsafe"] > 0.6:
            await event.delete()
        os.remove(file_path)
    except Exception as e:
        print("Error in dn_handler:", e)
