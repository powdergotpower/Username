from bot_client import client
import asyncio

# Track ongoing mentions per chat
ongoing_mentions = {}

@client.on(events.NewMessage(pattern=r'^/all(?:\s+(.*))?'))
async def all_command(event):
    chat = await event.get_chat()
    sender = await event.get_sender()

    # Only admins
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    text = event.pattern_match.group(1) or "Hey everyone!"
    members = await client.get_participants(chat)
    total = len(members)

    # Batch size based on total members
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
        if not ongoing_mentions.get(chat.id):
            break

        batch = members[i:i+batch_size]
        mentions = []
        for m in batch:
            if m.username:
                mentions.append(f"@{m.username}")
            else:
                mentions.append(f"[{m.first_name}](tg://user?id={m.id})")

        await client.send_message(chat, f"{' '.join(mentions)}\n\n{text}", parse_mode='md')
        await asyncio.sleep(3)

    ongoing_mentions[chat.id] = False
