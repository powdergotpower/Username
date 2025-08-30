import asyncio
from telegram import Update
from telegram.ext import ContextTypes

# Calculate batch size based on total members
def calculate_batch_size(total):
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

# /all command
async def all_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    # ✅ Fetch admins and check permissions
    admins = await context.bot.get_chat_administrators(chat.id)
    admin_ids = [admin.user.id for admin in admins]
    if user.id not in admin_ids:
        await update.message.reply_text("❌ Only admins can use this command.")
        return

    # ✅ Get message text
    message_text = " ".join(context.args) if context.args else "Hey everyone!"

    # ✅ Fetch all known members (for now: admins only, you can expand later)
    members = [admin.user for admin in admins]
    total_members = len(members)
    batch_size = calculate_batch_size(total_members)

    await update.message.reply_text(
        f"👥 Tagging {total_members} members in batches of {batch_size}..."
    )

    # ✅ Mention members in batches
    for i in range(0, total_members, batch_size):
        batch = members[i:i + batch_size]
        mentions_list = []

        for m in batch:
            if m.username:
                mentions_list.append(f"@{m.username}")
            else:
                mentions_list.append(f"[{m.first_name}](tg://user?id={m.id})")

        mentions_text = " ".join(mentions_list)
        try:
            await context.bot.send_message(
                chat.id,
                f"{mentions_text}\n\n{message_text}",
                parse_mode="Markdown"
            )
        except Exception as e:
            print("Error sending message:", e)

        await asyncio.sleep(5)  # delay between batches
