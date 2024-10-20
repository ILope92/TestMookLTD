
from sqlalchemy import Boolean, Column, ForeignKey, VARCHAR, Integer, String, Text, func
from sqlalchemy.orm import AppenderQuery, defer, relationship
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database.base import BaseDBModel, BaseCreatedUpdatedAtModel


class User(BaseDBModel, BaseCreatedUpdatedAtModel):
    __tablename__ = "users"
    
    login: Mapped[str] = mapped_column(String, nullable=False)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)


class Message(BaseDBModel, BaseCreatedUpdatedAtModel):
    __tablename__ = "messages"
    
    text = Column(Text, nullable=False, unique=False)
    sender_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    recipient_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))