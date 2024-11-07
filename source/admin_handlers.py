from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from create_bot import bot

import sqlite3 as sq

from source.general_config import ads, file_path, is_admin

'''
файл для объявления хендлеров для админа

например, расссылка или подсчёт количества пользователей
'''

class AdminState(StatesGroup): #статус для админа
    admin_panel = State()

def send_main_manu_admin(): #объявление клавиатуры для админа
    button1 = KeyboardButton("Пятёрочка")
    button2 = KeyboardButton("Магнит")
    button3 = KeyboardButton("/adversting")
    button4 = KeyboardButton("/count_users")
    
    geo_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button1).add(button2).add(button3).add(button4)
    return geo_kb


async def create_add(message: types.Message, state:FSMContext): #рассылка рекламы
    await message.delete()
    db_users = sq.connect(file_path[0])
    cur = db_users.cursor()
    cur.execute("SELECT userID FROM users_info WHERE code == 0")
    IDs = cur.fetchall()
    for item in IDs:
        await bot.send_message(chat_id=item[0],text=ads,reply_markup=InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='❌❌❌', callback_data='close')]]))
    db_users.close()
    async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id, message_id=data["last_msg"])
            msg = await bot.send_message(chat_id=message.from_id,text="реклама разослана!",reply_markup=send_main_manu_admin())
            data['last_msg'] = msg.message_id

async def count_users(message: types.Message, state:FSMContext): #подсчёт пользователй
    await message.delete()
    db_users = sq.connect(file_path[0])
    cur = db_users.cursor()
    cur.execute("SELECT userID FROM users_info WHERE code == 0")
    async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id, message_id=data["last_msg"])
            msg = await bot.send_message(chat_id=message.from_id,text=f'Всего {len(cur.fetchall())} пользователей!',reply_markup=send_main_manu_admin())
            data['last_msg'] = msg.message_id
    db_users.close()

async def close_ads(callback: types.CallbackQuery): #обработка callback запроса на закрытие рекламы
    if callback.data == 'close':
        await bot.delete_message(chat_id=callback.from_user.id,message_id=callback.message.message_id)


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(create_add,commands=['adversting'], state=AdminState.admin_panel)
    dp.register_message_handler(count_users,commands=['count_users'], state=AdminState.admin_panel)

    dp.register_callback_query_handler(close_ads,state='*')