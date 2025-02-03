import discord
import asyncio
import logging
from discord.ext import commands
from database import DatabaseManager
from views import AcceptCoachingPostButton


class MyBot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(command_prefix=None, intents=intents)
        self.db_manager = DatabaseManager()

    async def setup_hook(self):
        self.add_dynamic_items(AcceptCoachingPostButton)
        try:
            await self.load_extension("cogs.commands")
            await self.load_extension("cogs.events")
            synced = await self.tree.sync()
            print(f"Synced {len(synced)} commands.")
        except Exception as e:
            print(f"Error during sync: {e}")


def get_discord_token(file_path: str = "DISCORD_TOKEN") -> str:
    try:
        with open(file_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print(f"Error: file '{file_path}' not found.")
        exit(1)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        handlers=[logging.StreamHandler(), logging.FileHandler('bot.log')])

    logger = logging.getLogger()
    intents = discord.Intents.default()
    intents.messages = True

    bot = MyBot(intents=intents)

    discord_token = get_discord_token()
    async with bot:
        await bot.start(discord_token)


if __name__ == "__main__":
    asyncio.run(main())
