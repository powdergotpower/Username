import os
from telethon import TelegramClient, events, Button
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

client = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ------------------ /start command ------------------
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not event.is_private:  # PM only
        return
    
    bot_name = (await client.get_me()).first_name
    welcome_text = (
        f"👋 Hello!\nI am **{bot_name}** 🤖\n\n"
        "I can help you manage Telegram groups efficiently.\n"
        "I can mention members, track active users, delete nudity content automatically, "
        "and more!\n\n"
        "Use the buttons below to learn more about my commands or about my owner."
    )

    buttons = [
        [Button.inline("Help 📖", b"help"), Button.inline("Owner 👤", b"owner")]
    ]
    
    await event.respond(welcome_text, buttons=buttons)

# ------------------ Inline button callbacks ------------------
@client.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help":
        help_text = (
            "📌 **Commands and Usage:**\n\n"
            "/all Hey — Mentions all members in the group in batches. Admins only.\n"
            "Example: `/all Hello everyone!`\n\n"
            "/stopall — Stops ongoing mention process.\n\n"
            "/mam — Shows ranking of most active members in the group.\n\n"
            "/dn on/off — Automatically deletes nudity content when turned on."
        )
        await event.edit(help_text)
    elif event.data == b"owner":
        owner_text = (
            "👤 **Owner Info:**\n\n"
            "Hey! This bot was built by @s1dh7 with love 🎀❤️\n"
            "Feel free to add this bot into your group.\n"
            "If you find any errors, feel free to tell me."
        )
        await event.edit(owner_text)
