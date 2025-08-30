from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from bot_client import client
import asyncio

ongoing_mentions = {}

# Dynamic batch size based on total members
def batch_size(total):
    if total <= 10: return 1
    elif total <= 50: return 2
    elif total <= 100: return 3
    elif total <= 500: return 5
    elif total <= 2000: return 10
    else: return 20

@client.on(events.NewMessage(pattern=r'^/all(?:\s+(.*))?'))
async def all_command(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins can run
    admins = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
    if sender.id not in [a.id for a in admins]:
        await event.reply("❌ Only admins can use this command.")
        return

    text = event.pattern_match.group(1) or "Hey everyone!"

    # Get all members
    members = await client.get_participants(chat)
    total = len(members)

    await event.reply(f"👥 Mentioning {total} members in batches...")
    ongoing_mentions[chat.id] = True

    size = batch_size(total)
    for i in range(0, total, size):
        if not ongoing_mentions.get(chat.id):
            await event.reply("⛔ Mentioning stopped!")
            break

        batch = members[i:i+size]
        mentions = []
        for m in batch:
            if m.username:
                mentions.append(f"@{m.username}")
            else:
                mentions.append(f"[{m.first_name}](tg://user?id={m.id})")

        await client.send_message(chat, f"{' '.join(mentions)}\n\n{text}", parse_mode='md')
        await asyncio.sleep(3)

    ongoing_mentions[chat.id] = False

@client.on(events.NewMessage(pattern='/stopall'))
async def stopall(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins
    admins = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
    if sender.id not in [a.id for a in admins]:
        await event.reply("❌ Only admins can use this command.")
        return

    if ongoing_mentions.get(chat.id):
        ongoing_mentions[chat.id] = False
        await event.reply("✅ Stopped ongoing mentions.")
    else:
        await event.reply("ℹ️ No ongoing mentions in this chat.")
