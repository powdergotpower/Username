from bot_client import client
import modules.start       # PM-only /start with Help & Owner buttons
import modules.mention     # /all and /stopall commands in groups

print("🤖 Bot is running...")
client.run_until_disconnected()
