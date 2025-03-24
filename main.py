import os
import logging
from dotenv import load_dotenv
import discord
from discord.ext import commands
import src.bot_commands as bot_commands

load_dotenv()

DEFAULT_LOG_LEVEL = os.environ.get("LOG_LEVEL") or logging.INFO
logging.getLogger().setLevel(DEFAULT_LOG_LEVEL)
logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

DISCORD_BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Create a bot instance with the prefix '!!'
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="!!", intents=intents, help_command=None)


@bot.event
async def on_ready():
    logging.info(f"Logged in as {bot.user} ({bot.user.id})")
    logging.info("Bot ready.")


@bot.event
async def on_connect():
    await bot_commands.setup(bot)


# Run the bot with the token
if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
