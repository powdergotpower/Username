from bot_client import client
import asyncio

# Dictionary to track ongoing mentions per chat
# key = chat.id, value = True/False
ongoing_mentions = {}

@client.on(events.NewMessage(pattern='/all'))
async def all_command(event):
    chat = await event.get_chat()
    sender = await event.get_sender()
    
    # Only admins can use this
    if not (await client.is_admin(chat, sender.id)):
        await event.reply("❌ Only admins can use this command.")
        return

    args = event.message.message.split(" ", 1)
    text = args[1] if len(args) > 1 else "Hey everyone!"

    # Fetch members
    members = await client.get_participants(chat)
    total = len(members)

    # Determine batch size
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

    ongoing_mentions[chat.id] = True  # flag to allow stopping

    # Send mentions in batches
    for i in range(0, total, batch_size):
        if not ongoing_mentions.get(chat.id):
            break  # stop if /stopall was called

        batch = members[i:i+batch_size]
        mentions = []
        for m in batch:
            if m.username:
                mentions.append(f"@{m.username}")
            else:
                mentions.append(f"[{m.first_name}](tg://user?id={m.id})")

        await client.send_message(chat, f"{' '.join(mentions)}\n\n{text}", parse_mode='md')
        await asyncio.sleep(3)  # 3 sec delay between batches

    ongoing_mentions[chat.id] = False  # reset flag after done
