import sqlalchemy
from sqlalchemy import create_engine, URL, text, Table, Column, Integer, String, MetaData, insert
from sqlalchemy.orm import Session, sessionmaker
from config import settings
import psycopg2


sync_engine = create_engine(url=settings.DATABASE_URL_psycopg,
                       echo=True,
                       pool_size=5,
                       max_overflow=10)

metadata_obj = MetaData()

transactions_table = Table(
    "transactions",
    metadata_obj,
    Column("transaction_id", Integer, primary_key=True),
    Column("discord_id", String),
    Column("delta_balance", Integer),
    schema="main"
)


def create_tables():
    metadata_obj.create_all(sync_engine)


def insert_data():
    with sync_engine.connect() as conn:
        stmt = insert(transactions_table).values(
            [
                {"discord_id": "0", "delta_balance": 500},
                {"discord_id": "0", "delta_balance": -200},
            ]
        )
        conn.execute(stmt)
        conn.commit()