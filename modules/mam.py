from bot_client import client
from telethon import events
from collections import Counter

# Track message activity per user in groups
activity_counter = Counter()

# Track every message in groups to count activity
@client.on(events.NewMessage(func=lambda e: e.is_group))
async def track_activity(event):
    activity_counter[event.sender_id] += 1

# /mam command: shows most active members
@client.on(events.NewMessage(pattern=r'^/mam(?:\s+(\d+))?'))
async def mam_command(event):
    # Default top count is 5 if not specified
    count = int(event.pattern_match.group(1) or 5)

    # Get most active members
    top_members = activity_counter.most_common(count)

    if not top_members:
        await event.reply("ℹ️ No activity tracked yet in this group.")
        return

    # Build a visually nice message
    msg = "🏆 **Most Active Members:**\n\n"
    for idx, (user_id, msgs) in enumerate(top_members, start=1):
        msg += f"**{idx}.** [User](tg://user?id={user_id}) — `{msgs}` messages 📊\n"

    msg += "\n💡 Use `/mam <number>` to see top N active members. Example: `/mam 10`"

    await event.reply(msg, parse_mode='md')
