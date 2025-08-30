from telethon import events, Button
from bot_client import client  # use the shared client

# PM-only /start command
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    if not event.is_private:
        return
    bot_name = (await client.get_me()).first_name
    welcome_text = (
        f"👋 Hello!\nI am **{bot_name}** 🤖\n\n"
        "I can assist you in managing your Telegram groups effectively.\n"
        "Tap the buttons below to explore my features and commands."
    )
    buttons = [
        [Button.inline("Help 📖", b"help"), Button.inline("Owner 👤", b"owner")]
    ]
    await event.respond(welcome_text, buttons=buttons)

# ------------------ Inline button callbacks ------------------
@client.on(events.CallbackQuery)
async def callback(event):
    if event.data == b"help":
        help_text = """📌 **Commands Info:**

/all (message) — Mentions all members of the group in batches. Only admins can use this command.
Example: `/all Hey everyone!`
The bot will mention members in small groups to avoid flooding, and the batch size adjusts automatically depending on the group size.

/stopall — Stops ongoing mentions.

/mam — Shows the most active members in the group.

/dn on/off — Deletes nudity automatically.
"""
        buttons = [[Button.inline("Back 🔙", b"back")]]
        await event.edit(help_text, buttons=buttons)
        
    elif event.data == b"owner":
        owner_text = """👤 **Owner Info:**

This bot was built by @s1dh7 ❤️
Feel free to add it to your group.
Report any issues to the owner.
"""
        buttons = [[Button.inline("Back 🔙", b"back")]]
        await event.edit(owner_text, buttons=buttons)
        
    elif event.data == b"back":
        # Show the main start menu again
        bot_name = (await client.get_me()).first_name
        welcome_text = (
            f"👋 Hello!\nI am **{bot_name}** 🤖\n\n"
            "I can assist you in managing your Telegram groups effectively.\n"
            "Tap the buttons below to explore my features and commands."
        )
        buttons = [
            [Button.inline("Help 📖", b"help"), Button.inline("Owner 👤", b"owner")]
        ]
        await event.edit(welcome_text, buttons=buttons)
