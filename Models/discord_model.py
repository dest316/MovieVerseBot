import sqlalchemy
from sqlalchemy import create_engine, URL, text, Table, Column, Integer, String, MetaData, insert, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase
from config import settings
from Models.user_orm import UserOrm
import psycopg2


sync_engine = create_engine(url=settings.DATABASE_URL_psycopg,
                       echo=True,
                       pool_size=5,
                       max_overflow=10)

async_engine = create_async_engine(url=settings.DATABASE_URL_asyncpg,
                                   echo=True)
async_session = async_sessionmaker(async_engine)
# metadata_obj = MetaData()

# transactions_table = Table(
#     "transactions",
#     metadata_obj,
#     Column("transaction_id", Integer, primary_key=True),
#     Column("discord_id", String),
#     Column("delta_balance", Integer),
#     schema="main"
# )


# def create_tables():
#     metadata_obj.create_all(sync_engine)


# def insert_data():
#     with sync_engine.connect() as conn:
#         stmt = insert(transactions_table).values(
#             [
#                 {"discord_id": "0", "delta_balance": 500},
#                 {"discord_id": "0", "delta_balance": -200},
#             ]
#         )
#         conn.execute(stmt)
#         conn.commit()


async def update_balance(discord_id: str, amount: int, is_absolute_assignment=False):
    async with async_session() as session:
        async with session.begin():
            # Поиск записи с данным discord_id
            stmt = select(UserOrm).where(UserOrm.discord_id == discord_id)
            result = await session.execute(stmt)
            founded_user = result.scalar_one_or_none()

            if founded_user:
                # Обновление существующей записи
                if not is_absolute_assignment:
                    founded_user.roll_balance += amount
                else:
                    founded_user.roll_balance = amount
            else:
                # Вставка новой записи
                user = UserOrm(discord_id=discord_id, roll_balance=amount)
                session.add(user)

            # Коммит изменений
            await session.commit()


async def get_balance(discord_id: str):
    async with async_session() as session:
        stmt = select(UserOrm).where(UserOrm.discord_id == discord_id)
        result = await session.execute(stmt)
        founded_user = result.scalar_one_or_none()
        if founded_user:
            return founded_user.roll_balance
        return 0


async def roll_transfer(sender_id: str, recipient_id: str, amount: int, total: int):
    async with async_session() as session:
        async with session.begin():
            if sender_id == recipient_id:
                return 407
            stmt = select(UserOrm).where(UserOrm.discord_id == sender_id)
            result = await session.execute(stmt)
            sender = result.scalar_one_or_none()
            if not sender or sender.roll_balance < total:
                return 402
            sender.roll_balance -= total
            stmt = select(UserOrm).where(UserOrm.discord_id == recipient_id)
            result = await session.execute(stmt)
            recipient = result.scalar_one_or_none()
            if recipient:
                recipient.roll_balance += amount
                await session.commit()
                return 200
            recipient = UserOrm(discord_id=recipient_id, roll_balance=amount)
            session.add(recipient)
            await session.commit()
            return 200
