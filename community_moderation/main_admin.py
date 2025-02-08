import asyncio
import logging

from aiogram import Bot, Dispatcher, F
# from aiogram.filters import CommandStart
from aiogram.types import Message

from .database.models import async_main

from .bot_instance import bot_admin
from .app.checker.start import r_app_checker_start
from .app.checker.callback_handlers import r_callback
from .app.scraper.start import r_scraper_start

async def main():
    await async_main()
    dp = Dispatcher()
    dp.include_routers(r_app_checker_start, r_callback)
    await dp.start_polling(bot_admin)

if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
