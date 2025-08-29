import asyncio
import os
from telegram import Update, ChatMember
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# Store activity {chat_id: {user_id: message_count}}
activity_log = {}

# Track messages
async def track_activity(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_chat.type not in ["group", "supergroup"]:
        return
    chat_id = update.effective_chat.id
    user = update.effective_user
    if user.is_bot:
        return
    if chat_id not in activity_log:
        activity_log[chat_id] = {}
    if user.id not in activity_log[chat_id]:
        activity_log[chat_id][user.id] = 0
    activity_log[chat_id][user.id] += 1

# Check if admin
async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

# /all command
async def mention_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        return

    if len(context.args) < 2:
        await update.message.reply_text("Usage: /all <count> <message>")
        return

    try:
        count = int(context.args[0])
    except ValueError:
        await update.message.reply_text("❌ First argument must be a number (count).")
        return

    text_to_send = " ".join(context.args[1:])
    chat_id = update.effective_chat.id

    if chat_id not in activity_log or not activity_log[chat_id]:
        await update.message.reply_text("⚠️ No active members recorded yet.")
        return

    sorted_users = sorted(activity_log[chat_id].items(), key=lambda x: x[1], reverse=True)
    top_users = sorted_users[:count]

    await update.message.reply_text(f"✅ Mentioning top {len(top_users)} active members...")

    for user_id, _ in top_users:
        mention = f"[user](tg://user?id={user_id}) {text_to_send}"
        try:
            await context.bot.send_message(chat_id, mention, parse_mode="Markdown")
        except Exception:
            continue
        await asyncio.sleep(3)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_activity))
    app.add_handler(CommandHandler("all", mention_all))
    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
