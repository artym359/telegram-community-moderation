from aiogram import Bot
from .config import TOKEN

if not TOKEN:
    raise RuntimeError(
        "MODERATION_BOT_TOKEN is not set. Copy .env.example to .env and configure a test bot."
    )

bot_scraper = Bot(token=TOKEN)
bot_admin = Bot(token=TOKEN)
