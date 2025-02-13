from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from ...database import requests as rq
from . import inline_keyboards as ikb
from ...bot_instance import bot_admin
from ...config import ADMIN_USERNAMES, PERMITTED_USERNAMES

r_app_checker_start = Router()

@r_app_checker_start.message(CommandStart())
async def start(message: Message):
    chat_id = message.chat.id
    acc = await rq.get_New()

    username = (message.from_user.username or "").lower()

    if username in PERMITTED_USERNAMES:
        if acc:
            chat = await bot_admin.get_chat(acc.tg_id)
            # print(name)
            kb = await ikb.clear_ban_kb(tg_id=acc.tg_id, chat_id=chat_id)
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
    else:
        await bot_admin.send_message(
                text="Access denied. Ask an administrator to grant access.",
                chat_id=chat_id,
            )


@r_app_checker_start.message(Command('addchat'))
async def addchat(message: Message):

    chat_id = message.chat.id

    # print(message.from_user.username)

    username = (message.from_user.username or "").lower()

    if username in ADMIN_USERNAMES:
        try:
            msg_split = message.text.split(' ')

            if len(msg_split) >= 3 and msg_split[1][0] == '@' and len(msg_split[1]) >= 1 and msg_split[2][0] == '@' and len(msg_split[2]) >= 1:
                in_Chats = await rq.in_Chats(chat_username=msg_split[1])
                if not in_Chats:
                    await rq.addto_Chats(chat_username=msg_split[1], admin_username=msg_split[2])
                    await bot_admin.send_message(
                        text="Сделано",
                        chat_id=chat_id,
                        )
                else:
                    await bot_admin.send_message(
                        text="Повторное добавление",
                        chat_id=chat_id,
                        )
            else:
                await bot_admin.send_message(
                text="Invalid format. Use: /addchat @chat @administrator",
                chat_id=chat_id,
                )
        except Exception as e:
            print(e)
            pass
    else:
        await bot_admin.send_message(
                text="You are not allowed to use this command.",
                chat_id=chat_id,
            )
