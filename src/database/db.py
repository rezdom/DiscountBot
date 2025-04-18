from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column

from typing import Annotated

from src.database.utils.config import settings

async_engine = create_async_engine(
    url=settings.get_async_dsn,
    echo=False,
    pool_size=10,
    max_overflow=10,
    )

async_session = async_sessionmaker(async_engine)

intpk = Annotated[int, mapped_column(primary_key=True)]

class Base(DeclarativeBase):
    type_annotation_map = {
        intpk: Integer(),
    }