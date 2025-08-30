from bot_client import client
from telethon import events

# We will use a shared dictionary to track which chats are being mentioned
from modules.all import ongoing_mentions  # this will be a set/dict in all.py

@client.on(events.NewMessage(pattern='/stopall'))
async def stopall(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    # Only allow admins to stop
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    # Stop the mentions
    if chat.id in ongoing_mentions:
        ongoing_mentions[chat.id] = False  # set flag to False
        await event.reply("✅ Stopped mentioning members.")
    else:
        await event.reply("ℹ️ No ongoing mentions in this chat.")
