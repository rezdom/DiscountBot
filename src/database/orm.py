import datetime
from sqlalchemy import insert, select

from src.database.db_models import User, Sklep, Product
from src.database.db import async_session
from src.database.utils.enum_models import UserRole, MarketGroups, ProductTypes

class AsyncUserOrm:
    @staticmethod
    async def add_user(user_id: int, user_name: str):
        new_user = User(telegram_username = user_name, telegram_id = user_id)
        async with async_session() as session:
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user
    
    @staticmethod
    async def to_admin(user_id: int):
        async with async_session() as session:
            stmt = select(User).where(User.telegram_id==user_id)
            user = (await session.scalars(stmt)).one_or_none()
            if user:
                user.role = UserRole.ADMIN
                await session.commit()
                await session.refresh(user)
            return user

    @staticmethod
    async def to_ban(user_id: int):
        async with async_session() as session:
            stmt = select(User).where(User.telegram_id==user_id)
            user = (await session.scalars(stmt)).one_or_none()
            if user:
                user.is_banned = True
                await session.commit()
                await session.refresh(user)
            return user
    @staticmethod
    async def to_unban(user_id: int):
        async with async_session() as session:
            stmt = select(User).where(User.telegram_id==user_id)
            user = (await session.scalars(stmt)).one_or_none()
            if user:
                user.is_banned = False
                await session.commit()
                await session.refresh(user)
            return user

class AsyncSklepOrm:
    @staticmethod
    async def add_sklep(type: MarketGroups, shop_id: str, address: str):
        new_sklep = Sklep(type=type, shop_id=shop_id, address=address)
        async with async_session() as session:
            session.add(new_sklep)
            await session.commit()
            await session.refresh(new_sklep)
            return new_sklep

    @staticmethod
    async def get_update_sklep(shop_id: str):
        flag = False
        async with async_session() as session:
            stmt = select(Sklep).where(Sklep.shop_id==shop_id)
            sklep = (await session.scalars(stmt)).one()
            if sklep.created_at < datetime.datetime.now() - datetime.timedelta(days=7):
                flag = True
        return flag
    
    @staticmethod
    async def get_sklep(address: str):
        async with async_session() as session:
            stmt = select(Sklep).where(Sklep.address==address)
            sklep = (await session.scalars(stmt)).one_or_none()
            return sklep
    
    @staticmethod
    async def del_sklep(shop_id: str):
        async with async_session() as session:
            stmt = select(Sklep).where(Sklep.shop_id==shop_id)
            sklep = (await session.scalars(stmt)).one_or_none()
            await session.delete(sklep)
            await session.commit()
            return sklep

class AsyncProductOrm:
    @staticmethod
    async def add_products(products_data: list[dict]):
        stmt = insert(Product).values(products_data)
        async with async_session() as session:
            await session.execute(stmt)
            await session.commit()