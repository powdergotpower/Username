from bot_client import client
from modules.all import ongoing_mentions
from telethon import events

@client.on(events.NewMessage(pattern='/stopall'))
async def stopall(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    # Only admins
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    if ongoing_mentions.get(chat.id):
        ongoing_mentions[chat.id] = False
        await event.reply("✅ Stopped mentioning members.")
    else:
        await event.reply("ℹ️ No ongoing mentions in this chat.")
