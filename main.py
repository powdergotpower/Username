from modules.all import client  # import the client from modules/all.py

# Start the bot
client.start()
print("Bot is running...")
client.run_until_disconnected()
