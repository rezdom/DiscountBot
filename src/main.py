from asyncio import run
from aiogram import Bot, Dispatcher

from src.bot.utils.config import settings
from src.bot.handlers import routers
from src.bot.middlewares.general_middlewares import AntiFloodMiddleware, BanCheckMiddleware

bot = Bot(token=settings.TOKEN)
dp = Dispatcher()

for router in routers:
    dp.include_router(router)

async def setup_middlewares(dp: Dispatcher):
    ban_mw = BanCheckMiddleware()
    flood_mw = AntiFloodMiddleware(cooldown_seconds=1, max_calls=3)

    dp.message.outer_middleware(ban_mw)
    dp.callback_query.outer_middleware(ban_mw)

    dp.message.outer_middleware(flood_mw)
    dp.callback_query.outer_middleware(flood_mw)

async def main():
    await setup_middlewares(dp)
    await dp.start_polling(bot)

if __name__ == "__main__":
    run(main())