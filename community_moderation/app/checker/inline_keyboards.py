from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def clear_ban_kb(tg_id: int, chat_id: int, message_id: int = 0):

    callback = '?' + str(tg_id) + '?' + str(chat_id) + '?' + str(message_id)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text='BAN 🟥', callback_data='BAN' + callback),
        InlineKeyboardButton(text='CLEAR 🟩', callback_data='CLEAR' + callback)]
        ], one_time_keyboard=True
    )

    return keyboard