from source.Magnit import config
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import sqlite3 as sq

'''
создание бота я вывел в отдельный модуль, так как во многих операциях
мне требовалось импортировать bot или dp. 

И если бы я оставил создание в
модуле main то я бы получал ошибку, связанную с бесконечным цыклом импортирования
'''

storage = MemoryStorage()
bot = Bot(config.TOKEN_API)
dp = Dispatcher(bot,
                storage=storage)
