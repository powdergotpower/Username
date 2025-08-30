import asyncio
from modules.all import all_command

async def main():
    await all_command()  # starts the bot and listens for /all

if __name__ == "__main__":
    asyncio.run(main())
