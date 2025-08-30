import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# Function to calculate how many users per batch based on group size
def calculate_batch_size(total):
    if total <= 10:
        return 1
    elif total <= 100:
        return 3
    elif total <= 500:
        return 5
    elif total <= 2000:
        return 10
    elif total <= 10000:
        return 15
    else:
        return 20

# /all command function
async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    # ✅ Only admins and owner can use this
    member = await context.bot.get_chat_member(chat.id, user.id)
    if member.status not in ["administrator", "creator"]:
        return  # Ignore if normal user sends the command

    # ✅ Extract message after /all
    if context.args:
        message_text = " ".join(context.args)
    else:
        message_text = "Hey everyone!"

    # ✅ Fetch members list
    members = []
    async for m in context.bot.get_chat_administrators(chat.id):  # right now admins only
        members.append(m.user)

    total = len(members)
    batch_size = calculate_batch_size(total)

    await update.message.reply_text(
        f"👥 Tagging {total} members in batches of {batch_size}..."
    )

    # ✅ Mention users in batches
    for i in range(0, total, batch_size):
        batch = members[i:i + batch_size]
        mentions_list = []

        for m in batch:
            if m.username:  # If user has a @username
                mentions_list.append(f"@{m.username}")
            else:  # Otherwise use clickable mention
                mentions_list.append(f"[{m.first_name}](tg://user?id={m.id})")

        mentions = " ".join(mentions_list)

        try:
            await context.bot.send_message(
                chat.id,
                f"{mentions}\n\n{message_text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print("Error while tagging:", e)

        await asyncio.sleep(5)  # Delay to avoid spam ban
