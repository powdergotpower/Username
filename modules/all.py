import os
import asyncio
from telethon import TelegramClient
from telethon.tl.types import ChannelParticipantsAdmins
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# Dynamic batch size
def batch_size(total):
    if total <= 10:
        return 1
    elif total <= 50:
        return 2
    elif total <= 100:
        return 3
    elif total <= 500:
        return 5
    elif total <= 2000:
        return 10
    else:
        return 20

async def all_command():
    @client.on(events.NewMessage(pattern='/all'))
    async def handler(event):
        chat = await event.get_chat()
        sender = await event.get_sender()
        # Only admins/creator can run
        if not (await client.is_admin(chat, sender.id)):
            await event.reply("❌ Only admins can use this command.")
            return

        # Get message text
        args = event.message.message.split(" ", 1)
        text = args[1] if len(args) > 1 else "Hey everyone!"

        # Fetch all participants
        members = await client.get_participants(chat)
        total = len(members)
        size = batch_size(total)

        await event.reply(f"👥 Tagging {total} members in batches of {size}...")

        # Send mentions in batches
        for i in range(0, total, size):
            batch = members[i:i+size]
            mentions = []
            for m in batch:
                if m.username:
                    mentions.append(f"@{m.username}")
                else:
                    mentions.append(f"[{m.first_name}](tg://user?id={m.id})")
            await client.send_message(chat, f"{' '.join(mentions)}\n\n{text}", parse_mode='md')
            await asyncio.sleep(5)

    await client.run_until_disconnected()
