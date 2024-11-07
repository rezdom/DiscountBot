from create_bot import dp
from source.Magnit import config
from source.Pyatorochka import config_pyat
   
from aiogram import executor

import sqlite3 as sq

from source.Magnit.magnit_handlers import client_handlers
from source.Pyatorochka.pyat_handlers import client_handlers_pyat
from source.admin_handlers import register_admin_handlers
from source.general_config import file_path
import general_cient_handlers

from middlewares import ThrottledMiddlware

'''
main - файл для запуска бота
'''

async def db_connect(): #функция для подключения баз данных
    global db_cities, cur_cities, db_cards, cur_cards, db_pyat_cards, cur_pyat_cards, db_users_info, cur_users_info
    db_cities = sq.connect(config.file_path[0])
    cur_cities = db_cities.cursor()
    db_cards = sq.connect(config.file_path[1])
    cur_cards = db_cards.cursor()
    db_pyat_cards = sq.connect(config_pyat.file_path[0])
    cur_pyat_cards = db_cards.cursor()
    db_users_info = sq.connect(file_path[0])
    cur_users_info = db_users_info.cursor()

async def on_startup(_): #функция, которая срабатывает при запуске бота
    print('Я начал работу')
    await db_connect()

client_handlers.register_handlers_client(dp) #подключаю хендлеры
client_handlers_pyat.register_pyat_handlers_client(dp)
general_cient_handlers.register_general_handlers(dp)
register_admin_handlers(dp)



if __name__ == "__main__":
    dp.middleware.setup(ThrottledMiddlware()) #установка мидлвари и запуск через экзекъютор
    executor.start_polling(dispatcher=dp,
                           skip_updates=True,
                           on_startup=on_startup)

