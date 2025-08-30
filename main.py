from bot_client import client
import modules.start  # attach the /start PM handler
# You can import group command modules later here, e.g., modules.all

print("Bot is running...")
client.run_until_disconnected()
