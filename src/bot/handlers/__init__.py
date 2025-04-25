from src.bot.handlers.general_handlers import router as general_router
from src.bot.handlers.magnit_handlers import router as magnit_router
from src.bot.handlers.pyatorochka_handlers import router as pyatorochka_router

routers = [general_router, magnit_router, pyatorochka_router]