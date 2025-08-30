from telethon import events
from telethon.tl.types import ChannelParticipantsAdmins
from collections import defaultdict

# Track per-group, per-user
group_user_messages = defaultdict(lambda: defaultdict(int))

@client.on(events.NewMessage())
async def track_messages(event):
    if not event.is_group:
        return
    group_id = event.chat_id
    sender = await event.get_sender()
    if sender:
        group_user_messages[group_id][sender.id] += 1

async def mam_stats(event, n):
    if not event.is_group:
        await event.reply("ℹ️ This command only works in groups.")
        return
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Admin check
    admins = await client.get_participants(chat, filter=ChannelParticipantsAdmins)
    admin_ids = [a.id for a in admins]
    if sender.id not in admin_ids:
        await event.reply("❌ Only admins can use this command.")
        return

    group_id = event.chat_id
    user_msgs = group_user_messages.get(group_id, {})
    if not user_msgs:
        await event.reply("🕓 I have to record messages first. Please try again after some time.")
        return

    # Sort users by activity
    sorted_users = sorted(user_msgs.items(), key=lambda x: x, reverse=True)
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

# /mam [default top 10]
@client.on(events.NewMessage(pattern=r'^/mam$'))
async def mam_command(event):
    await mam_stats(event, 10)

# /mam1 [top 1]
@client.on(events.NewMessage(pattern=r'^/mam1$'))
async def mam1_command(event):
    await mam_stats(event, 1)
