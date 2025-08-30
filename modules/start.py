from telethon import events, Button
from modules.all import client  # import the existing client

# ------------------ /start command ------------------
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not event.is_private:  # PM only
        return
    
    bot_name = (await client.get_me()).first_name
    welcome_text = (
        f"👋 Hello!\nI am **{bot_name}** 🤖\n\n"
        "I can help you manage Telegram groups efficiently.\n"
        "Here you will find information about my commands and owner.\n\n"
        "Use the buttons below to learn more."
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
            "📌 **Commands Info:**\n\n"
            "/all Hey — Mentions all members in a group in batches. Admins only.\n"
            "/stopall — Stops ongoing mention process.\n"
            "/mam — Shows ranking of most active members in the group.\n"
            "/dn on/off — Automatically deletes nudity content when turned on.\n\n"
            "This section is only informational and does not run in PM."
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
