import os

from sqlalchemy import BigInteger, Boolean, String

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

DATABASE_URL = os.getenv(
    "MODERATION_DATABASE_URL",
    "sqlite+aiosqlite:///data/moderation.sqlite3",
).strip()

engine = create_async_engine(url=DATABASE_URL)

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class New(Base):
    # Новые id, не находящиеся в banned или находящиеся в cleared меньше дельты
    __tablename__ = 'New'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    chat_id: Mapped[int] = mapped_column(BigInteger)
    message_id: Mapped[int] = mapped_column(BigInteger)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class Banned(Base):
    __tablename__ = 'Banned'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)

class Cleared(Base):
    __tablename__ = 'Cleared'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    date_cleared: Mapped[str] = mapped_column(String)

class Chats(Base):
    __tablename__ = 'Chats'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    chat_username: Mapped[str] = mapped_column(String)
    admin_username: Mapped[str] = mapped_column(String)
    n_checked: Mapped[int] = mapped_column(BigInteger)
    n_banned: Mapped[int] = mapped_column(BigInteger)

    date_paid: Mapped[str] = mapped_column(String)
    is_paid: Mapped[bool] = mapped_column(Boolean)


async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
