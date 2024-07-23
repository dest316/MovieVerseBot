from sqlalchemy import Table, Column, Integer, String, MetaData
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class UserOrm(Base):
    __tablename__ = "users_balance"
    __table_args__ = {"schema": "main"}
    local_id: Mapped[int] = mapped_column(primary_key=True)
    discord_id: Mapped[str]
    roll_balance: Mapped[int]
