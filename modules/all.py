from telethon import events
from telethon.tl.types import ChannelParticipantsSearch
from bot_client import client
import asyncio

# Track ongoing mentions per chat
ongoing_mentions = {}

@client.on(events.NewMessage(pattern=r'^/all(?:\s+(.*))?'))
async def all_command(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins can use
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    text = event.pattern_match.group(1) or "Hey everyone!"

    # Fetch all members properly
    members = await client.get_participants(chat, filter=ChannelParticipantsSearch(''))
    total = len(members)

    if total == 0:
        await event.reply("⚠️ Cannot fetch members. Make sure the bot is in the group and has permission.")
        return

    # Determine batch size dynamically
    if total <= 10:
        batch_size = 1
    elif total <= 50:
        batch_size = 2
    elif total <= 100:
        batch_size = 3
    elif total <= 500:
        batch_size = 5
    elif total <= 2000:
        batch_size = 10
    else:
        batch_size = 20

    await event.reply(f"👥 Mentioning {total} members in batches of {batch_size}...")
    ongoing_mentions[chat.id] = True

    for i in range(0, total, batch_size):
        # Stop if /stopall was called
        if not ongoing_mentions.get(chat.id):
            await event.reply("⛔ Mentioning stopped!")
            break

        batch = members[i:i+batch_size]
        mentions = [
            f"@{m.username}" if m.username else f"[{m.first_name}](tg://user?id={m.id})"
            for m in batch
        ]

        await client.send_message(chat, f"{' '.join(mentions)}\n\n{text}", parse_mode='md')
        await asyncio.sleep(3)  # 3 sec between batches

    ongoing_mentions[chat.id] = False

# ------------------------------
# /stopall command
# ------------------------------
@client.on(events.NewMessage(pattern='/stopall'))
async def stopall(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins can use
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    if ongoing_mentions.get(chat.id):
        ongoing_mentions[chat.id] = False
        await event.reply("✅ Stopped ongoing mentions.")
    else:
        await event.reply("ℹ️ No ongoing mentions in this chat.")
