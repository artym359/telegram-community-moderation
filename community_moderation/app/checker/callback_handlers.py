from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
# from aiogram.filters import CommandStart
from ...database import requests as rq
from aiogram.types import ReplyKeyboardRemove

from . import functions as f
from ...bot_instance import bot_admin

r_callback = Router()


@r_callback.callback_query(lambda callback: callback.data)
async def callback_handler(callback: CallbackQuery):
    data = callback.data
    if data.startswith('BAN'):
        data_info=data.split('?')
        await rq.addto_Banned(tg_id=int(data_info[1]))
        acc = await rq.get_New_by_tg_id(tg_id=int(data_info[1]))
        try:
            await bot_admin.delete_message(message_id=acc['message_id'], chat_id=acc['chat_id'])
            await bot_admin.ban_chat_member(chat_id=acc['chat_id'], user_id=acc['tg_id'])
        except Exception as e:
            print(e)
            pass
        await rq.delfrom_New(tg_id=int(data_info[1]))
        chat = await bot_admin.get_chat(chat_id=acc['chat_id'])
        await rq.increase_checked_Chats(chat_username=f'@{chat.username}', increase_banned=True)
        await callback.message.delete()
        await f.next_acc(int(data_info[2]))

    elif data.startswith('CLEAR'):
        data_info=data.split('?')
        acc = await rq.get_New_by_tg_id(tg_id=int(data_info[1]))
        chat = await bot_admin.get_chat(chat_id=acc['chat_id'])
        await rq.addto_Cleared(tg_id=int(data_info[1]))
        await rq.delfrom_New(tg_id=int(data_info[1]))
        await rq.increase_checked_Chats(chat_username=f'@{chat.username}', increase_banned=False)
        await callback.message.delete()

        await f.next_acc(int(data_info[2]))
