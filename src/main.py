from asyncio import run
from aiogram import Bot, Dispatcher

from src.bot.utils.config import settings
from src.bot.handlers import routers

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

for router in routers:
    dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())