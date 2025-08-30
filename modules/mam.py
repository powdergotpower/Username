from bot_client import client
from telethon import events
from collections import defaultdict, Counter
from datetime import datetime, timedelta

# Store activity per user with timestamp
activity_log = defaultdict(list)

# Track all messages in groups
@client.on(events.NewMessage(func=lambda e: e.is_group))
async def track_activity(event):
    user_id = event.sender_id
    timestamp = datetime.now()
    activity_log[user_id].append(timestamp)

# Function to count messages in a given time period
def count_messages(timestamps, period_days=None):
    now = datetime.now()
    if period_days:
        return sum(1 for t in timestamps if now - t <= timedelta(days=period_days))
    return len(timestamps)  # Total messages

# /mam command
@client.on(events.NewMessage(pattern=r'^/mam(?:\s+(\d+))?'))
async def mam_command(event):
    top_n = int(event.pattern_match.group(1) or 5)
    chat = await event.get_chat()

    # Build stats
    stats = {
        "Daily 🌞": {},
        "Weekly 📅": {},
        "Monthly 📆": {},
        "Total 🏆": {}
    }

    for user_id, timestamps in activity_log.items():
        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "Unknown"
        except:
            name = "Unknown"

        stats["Daily 🌞"][name] = count_messages(timestamps, 1)
        stats["Weekly 📅"][name] = count_messages(timestamps, 7)
        stats["Monthly 📆"][name] = count_messages(timestamps, 30)
        stats["Total 🏆"][name] = count_messages(timestamps, None)

    # Build the message
    msg = f"📊 **Top Active Members in {chat.title}**\n\n"
    for period, data in stats.items():
        if not data:
            continue
        msg += f"__{period}__\n"
        top = Counter(data).most_common(top_n)
        for idx, (name, msgs) in enumerate(top, start=1):
            msg += f"**{idx}. {name}** — `{msgs}` messages\n"
        msg += "\n"

    msg += f"💡 Use `/mam <number>` to see top N members. Example: `/mam 10`"

    await event.reply(msg, parse_mode='md')
