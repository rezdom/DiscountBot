from sqlalchemy import text, ForeignKey, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.database.db import Base, intpk
from src.database.utils.enum_models import UserRole, MarketGroups, ProductTypes


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    telegram_username: Mapped[str]
    telegram_id: Mapped[int]
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc-3', now())"))
    update_at: Mapped[datetime] = mapped_column(
        server_default=text("TIMEZONE('utc-3', now())"),
        onupdate=text("TIMEZONE('utc-3', now())"),
        )
    is_banned: Mapped[bool] = mapped_column(default=False)

class Sklep(Base):
    __tablename__ = "sklepy"

    id: Mapped[intpk]
    type: Mapped[MarketGroups] = mapped_column(Enum(MarketGroups))
    shop_id: Mapped[str]
    address: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc-3', now())"))

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger(), primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("sklepy.id", ondelete="CASCADE"))
    product_type: Mapped[ProductTypes] = mapped_column(Enum(ProductTypes))
    name: Mapped[str]
    price: Mapped[float]
    discount: Mapped[int]