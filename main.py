from bot_client import client

# Import all command modules
import modules.start       # PM-only /start
import modules.mention     # /all and /stopall
import modules.mam         # /mam
import modules.dn          # /dn on/off

print("🤖 Bot is running... Listening for /start in PM and other commands in groups.")
client.run_until_disconnected()
