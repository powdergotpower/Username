from telethon import events, Button
from bot_client import client
from collections import defaultdict, Counter
from datetime import datetime, timedelta
import json
import asyncio
import os

# ----- Persistent storage -----
activity_file = "activity.json"
activity_log = defaultdict(list)

# Load JSON on startup
def load_activity():
    if os.path.exists(activity_file):
        try:
            with open(activity_file, "r") as f:
                data = json.load(f)
                for uid, times in data.items():
                    activity_log[int(uid)] = [datetime.fromisoformat(t) for t in times]
        except:
            print("⚠️ Failed to load activity.json")

# Save JSON
def save_activity():
    data = {str(uid): [t.isoformat() for t in times] for uid, times in activity_log.items()}
    with open(activity_file, "w") as f:
        json.dump(data, f)

# Auto-save periodically every 60 seconds
async def autosave_loop():
    while True:
        await asyncio.sleep(60)
        save_activity()

# ----- Track all group messages -----
@client.on(events.NewMessage(func=lambda e: e.is_group))
async def track_activity(event):
    uid = event.sender_id
    activity_log[uid].append(datetime.now())
    # Optional: save every message
    # save_activity()

# ----- Helper to count messages for period -----
def count_messages(timestamps, days=None):
    now = datetime.now()
    if days:
        return sum(1 for t in timestamps if now - t <= timedelta(days=days))
    return len(timestamps)

# ----- Build ranking message -----
async def build_mam_message(event, period_days, period_name):
    chat = await event.get_chat()
    stats = {}

    for user_id, timestamps in activity_log.items():
        # Skip users with no messages in period
        if period_days and all(datetime.now() - t > timedelta(days=period_days) for t in timestamps):
            continue
        try:
            user = await client.get_entity(user_id)
            name = user.first_name or "Unknown"
        except:
            name = "Unknown"
        stats[name] = count_messages(timestamps, period_days)

    if not stats:
        return f"ℹ️ No activity tracked yet in **{chat.title}**."

    top_members = Counter(stats).most_common(10)
    msg = f"📊 **Top Active Members — {period_name}**\n\n"
    for idx, (name, msgs) in enumerate(top_members, start=1):
        msg += f"**{idx}. {name}** — `{msgs}` messages\n"
    return msg

# ----- /mam command -----
@client.on(events.NewMessage(pattern=r'^/mam$'))
async def mam_command(event):
    msg = await build_mam_message(event, 1, "Today 🌞")
    buttons = [
        [Button.inline("Weekly 📅", b"weekly"), Button.inline("Monthly 📆", b"monthly"), Button.inline("Total 🏆", b"total")]
    ]
    await event.reply(msg, buttons=buttons, parse_mode='md')

# ----- Handle inline button clicks -----
@client.on(events.CallbackQuery)
async def mam_buttons(event):
    if event.data == b"weekly":
        msg = await build_mam_message(event, 7, "This Week 📅")
    elif event.data == b"monthly":
        msg = await build_mam_message(event, 30, "This Month 📆")
    elif event.data == b"total":
        msg = await build_mam_message(event, None, "Total 🏆")
    else:
        return

    await event.edit(msg, buttons=[
        [Button.inline("Weekly 📅", b"weekly"), Button.inline("Monthly 📆", b"monthly"), Button.inline("Total 🏆", b"total")]
    ], parse_mode='md')

# ----- Start autosave loop -----
asyncio.create_task(autosave_loop())
load_activity()
