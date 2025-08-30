import os
from telegram.ext import Application, CommandHandler
from modules.all import all_command  # ✅ import our command

TOKEN = os.getenv("BOT_TOKEN")

def main():
    app = Application.builder().token(TOKEN).build()

    # ✅ register /all command
    app.add_handler(CommandHandler("all", all_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
