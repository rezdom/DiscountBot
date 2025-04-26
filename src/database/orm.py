import datetime
from sqlalchemy import insert, select

from src.database.db_models import User, Sklep, Product, Report
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
    async def get_user(user_id: int):
        async with async_session() as session:
            stmt = select(User).where(User.telegram_id==user_id)
            return (await session.scalars(stmt)).one_or_none()
    
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
            sklep = (await session.scalars(stmt)).one_or_none()
            if sklep and sklep.created_at < datetime.datetime.now() - datetime.timedelta(days=7):
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
    
    @staticmethod
    async def get_products(sklep_id: int, product_type:ProductTypes, discount: int):
        async with async_session() as session:
            stmt = select(Product).where(
                (Product.shop_id == sklep_id) &
                (Product.product_type == product_type) &
                (Product.discount >= discount)
            )
            products_list = (await session.scalars(stmt)).all()
            return products_list

class AsyncReportOrm:
    @staticmethod
    async def add_report(user_id: int, telegram_id:int, report: str):
        new_report = Report(user_id=user_id, report=report, telegram_id=telegram_id)
        async with async_session() as session:
            session.add(new_report)
            await session.commit()
            await session.refresh(new_report)
            return new_report
    
    @staticmethod
    async def pop_report():
        stmt = select(Report).order_by(Report.id.desc())
        async with async_session() as session:
            last_report = (await session.scalars(stmt)).first()

            if last_report:
                await session.delete(last_report)
                await session.commit()

            return last_report
    
    @staticmethod
    async def get_len_reports():
        stmt = select(Report)
        async with async_session() as session:
            return len((await session.scalars(stmt)).all())