import asyncio
import logging

from aiogram import Bot, Dispatcher, F
# from aiogram.filters import CommandStart
from aiogram.types import Message

from .database.models import async_main

from .bot_instance import bot_scraper
from .app.scraper.start import r_scraper_start

async def main():
    await async_main()
    dp = Dispatcher()
    dp.include_router(r_scraper_start)
    await dp.start_polling(bot_scraper)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
