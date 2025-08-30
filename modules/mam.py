from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from bot_client import client
from collections import defaultdict

# In-memory message tracking
user_messages = defaultdict(int)

# Track messages for activity
@client.on(events.NewMessage())
async def track_messages(event):
    if not event.is_group:
        return
    sender = await event.get_sender()
    if sender:  # Make sure sender exists
        user_messages[sender.id] += 1

# /mam command
@client.on(events.NewMessage(pattern=r'^/mam(?:\s+(\d+))?$'))
async def mam_command(event):
    if not event.is_group:
        await event.reply("ℹ️ This command only works in groups.")
        return

    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins
    admins = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
    admin_ids = [a.id for a in admins]
    if sender.id not in admin_ids:
        await event.reply("❌ Only admins can use this command.")
        return

    # Get top N from command, default 10
    n_str = event.pattern_match.group(1)
    try:
        n = int(n_str) if n_str else 10
        if n <= 0:
            n = 10
    except:
        n = 10

    if not user_messages:
        await event.reply("ℹ️ No messages tracked yet in this group.")
        return

    # Sort users by messages
    sorted_users = sorted(user_messages.items(), key=lambda x: x[1], reverse=True)
    top_n = sorted_users[:n]

    text = f"📊 **Top {len(top_n)} Most Active Members:**\n\n"
    for idx, (user_id, count) in enumerate(top_n, start=1):
        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "User"
            text += f"{idx}. [{name}](tg://user?id={user_id}) — {count} messages\n"
        except:
            text += f"{idx}. UserID {user_id} — {count} messages\n"

    await event.reply(text, parse_mode="md")
