from .models import async_session
from .models import New, Cleared, Banned, Chats
from sqlalchemy import select, update, and_, delete
from datetime import datetime, timezone



"""
Проверка нахождения аккаунта в таблице
"""

async def in_Banned(tg_id: int) -> bool:
    async with async_session() as session:
        acc = await session.scalar(select(Banned).where(Banned.tg_id == tg_id))
    if acc:
        return True
    else:
        return False

async def in_New(tg_id: int) -> bool:
    async with async_session() as session:
        acc = await session.scalar(select(New).where(New.tg_id == tg_id))
    if acc:
        return True
    else:
        return False

async def in_Cleared(tg_id: int) -> bool:
    async with async_session() as session:
        acc = await session.scalar(select(Cleared).where(Cleared.tg_id == tg_id))
    if acc:
        return True
    else:
        return False

async def in_Chats(chat_username: str) -> bool:
    async with async_session() as session:
        acc = await session.scalar(select(Chats).where(Chats.chat_username == chat_username))
        # print(acc)
    if acc:
        return True
    else:
        return False

"""
Добавление аккаунта в таблицу
"""
async def addto_Cleared(tg_id: int):
    async with async_session() as session:
        session.add(Cleared(tg_id=tg_id, date_cleared=str(datetime.now(timezone.utc))))
        await session.commit()

async def addto_New(tg_id: int, chat_id: int, message_id: int):
    async with async_session() as session:
        session.add(New(tg_id=tg_id, chat_id=chat_id, message_id=message_id))
        await session.commit()

async def addto_Banned(tg_id: int):
    async with async_session() as session:
        session.add(Banned(tg_id=tg_id))
        await session.commit()

async def addto_Chats(chat_username: str, admin_username: str):
    async with async_session() as session:
        session.add(Chats(chat_username=chat_username, admin_username=admin_username, n_checked=0, n_banned=0, date_paid=str(datetime.now(timezone.utc)), is_paid=True))
        await session.commit()

"""""
Удаление аккаунта из таблицы
"""""
async def delfrom_Banned(tg_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Banned).where(Banned.tg_id == tg_id)
        )
        await session.commit()

async def delfrom_New(tg_id: int):
    async with async_session() as session:
        await session.execute(
            delete(New).where(New.tg_id == tg_id)
        )
        await session.commit()

async def delfrom_Cleared(tg_id: int):
    async with async_session() as session:
        await session.execute(
            delete(Cleared).where(Cleared.tg_id == tg_id)
        )
        await session.commit()


"""""
Получение первого образца из таблицы
"""""

async def get_New():
    async with async_session() as session:
        query = await session.execute(select(New).limit(1))
        acc = query.scalars().first()
        if acc:
            return acc
        else:
            return False

async def get_New_by_tg_id(tg_id: int):
    async with async_session() as session:
        async with async_session() as session:
            acc = await session.scalar(select(New).where(New.tg_id == tg_id))
            if acc:
                return acc.as_dict()
            else:
                return False


"""""
Инкремент одного из параметров
"""""




async def increase_checked_Chats(chat_username: str, increase_banned: bool = False):
    async with async_session() as session:
        acc = await session.scalar(select(Chats).where(Chats.chat_username == chat_username))

        if acc:
            acc.n_checked += 1

            if increase_banned:
                acc.n_banned += 1

            await session.commit()
