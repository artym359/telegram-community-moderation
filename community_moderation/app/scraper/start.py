from aiogram import types, Router, F
import re

from ...database import requests as rq
from ...bot_instance import bot_scraper

def contains_url(s) -> bool:
    if s is None:
        return False
    url_pattern = re.compile(r'\b(?:https?://|www\.|[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})[\w./?=&%-]*')
    return bool(url_pattern.search(s))

r_scraper_start = Router()

@r_scraper_start.message(F.chat.type.in_(['group', 'supergroup']))
async def parse_messages(message: types.Message):
    chat_username = message.chat.username

    in_Chats = await rq.in_Chats(chat_username=f'@{chat_username}')

    # print(in_Chats)

    if in_Chats:
        if message.sender_chat and (not (message.sender_chat and message.sender_chat.id == message.bot.id)) and (message.sender_chat.id != message.chat.id):
            pass
            # The message is intentionally ignored when it comes from a bot/system sender.
        else:
                chat = await bot_scraper.get_chat(message.from_user.id)

                if contains_url(chat.bio) or chat.linked_chat_id is not None:
                    acc_id = message.from_user.id
                    in_New = await rq.in_New(tg_id=acc_id)

                    if not in_New:
                        in_Banned = await rq.in_Banned(tg_id=acc_id)
                        if in_Banned:
                            await bot_scraper.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id)
                            try:
                                await bot_scraper.delete_message(chat_id=message.chat.id, message_id=message.message_id)
                            except Exception:
                                pass
                        else:
                            in_Cleared = await rq.in_Cleared(tg_id=acc_id)
                            if in_Cleared:
                                pass
                            else:
                                await rq.addto_New(tg_id=acc_id, chat_id=message.chat.id, message_id=message.message_id)
    else:
        pass
