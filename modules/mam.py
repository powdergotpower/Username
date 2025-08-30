from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from bot_client import client
from collections import Counter
import asyncio

# In-memory message tracking
user_messages = {}

# Track messages for activity
@client.on(events.NewMessage())
async def track_messages(event):
    if not event.is_group:
        return
    sender = await event.get_sender()
    user_messages[sender.id] = user_messages.get(sender.id, 0) + 1

# /mam command with dynamic top N
@client.on(events.NewMessage(pattern=r'^/mam(?:\s+(\d+))?'))
async def mam_command(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins
    admins = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
    if sender.id not in [a.id for a in admins]:
        await event.reply("❌ Only admins can use this command.")
        return

    # Get number of top members, default 10
    n = event.pattern_match.group(1)
    try:
        n = int(n)
        if n <= 0:
            n = 10
    except:
        n = 10

    if not user_messages:
        await event.reply("ℹ️ No messages tracked yet in this group.")
        return

    # Sort users by message count
    sorted_users = sorted(user_messages.items(), key=lambda x: x[1], reverse=True)
    
    # Take top n
    top_n = sorted_users[:n]

    text = f"📊 **Top {len(top_n)} Most Active Members:**\n\n"
    for idx, (user_id, count) in enumerate(top_n, start=1):
        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "User"
            text += f"{idx}. [{name}](tg://user?id={user_id}) — {count} messages\n"
        except:
            continue

    await event.reply(text, parse_mode="md")
