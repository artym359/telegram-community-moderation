from aiogram.types import Message

from ...bot_instance import bot_admin
from . import inline_keyboards as ikb
from ...database import requests as rq

async def next_acc(chat_id: int):
    acc = await rq.get_New()

    if acc:
        kb = await ikb.clear_ban_kb(tg_id=acc.tg_id, chat_id=chat_id, message_id=acc.message_id)
        chat = await bot_admin.get_chat(acc.tg_id)
        # print(chat.full_name)
        await bot_admin.send_message(
            text=f'@{chat.username}\n{chat.full_name}\n{chat.bio}\n{chat.linked_chat_id}',
            reply_markup=kb,
            chat_id=chat_id,
        )
    else:
        await bot_admin.send_message(
            text="Не осталось непроверенных анкет, проверьте позже",
            chat_id=chat_id,
        )
