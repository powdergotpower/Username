from telethon import events, Button
from bot_client import client  # use the shared client

# PM-only start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not event.is_private:
        return
    bot_name = (await client.get_me()).first_name
    welcome_text = (
        f"👋 Hello!\nI am **{bot_name}** 🤖\n\n"
        "I can help you manage Telegram groups efficiently.\n"
        "Use the buttons below to learn more."
    )
    buttons = [
        [Button.inline("Help 📖", b"help"), Button.inline("Owner 👤", b"owner")]
    ]
    await event.respond(welcome_text, buttons=buttons)

@client.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help":
        text = (
            "📌 **Commands Info:**\n"
            "/all — Mentions members in batches (admins only).\n"
            "/stopall — Stops ongoing mentions.\n"
            "/mam — Shows most active members.\n"
            "/dn on/off — Deletes nudity automatically.\n\n"
            "(This is PM-only informational help.)"
        )
        await event.edit(text)
    elif event.data == b"owner":
        text = (
            "👤 **Owner Info:**\n"
            "This bot was built by @s1dh7 ❤️\n"
            "Feel free to add it to your group.\n"
            "Report any issues to the owner."
        )
        await event.edit(text)
