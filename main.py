import os
from telegram.ext import Application, CommandHandler
from modules.all import all_command
from dotenv import load_dotenv  # ✅ add this

# Load environment variables from .env
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")  # now this will read your token from .env

def main():
    app = Application.builder().token(TOKEN).build()

    # Register /all command
    app.add_handler(CommandHandler("all", all_command))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
