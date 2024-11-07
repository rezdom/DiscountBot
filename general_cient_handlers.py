from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from create_bot import bot

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

import sqlite3 as sq

from source.general_config import is_admin
from source.Magnit import keyboards
from source.Magnit import config

from source.admin_handlers import send_main_manu_admin, AdminState

'''
general_client_handlers - модуль для  объявления основных хендлеров
такие как обработка команды 'start' или  перехода в режими прасинга
пятёрочки или магнита
'''

HELP_DESC = ''' 
Привет, я разработал данного бота, чтобы помочь вам найти лучшие цены!\n

Данный бот обладает следующими коммандами:\n

<b>start</b> - команда для запуска бота, а так же чтобы вернуться в главное меню из любого состояния, если вдруг произошла какая либо ошибка\n
<b>help</b> - краткое описание того, что умеет этот бот\n

Ну а дальше всё ясно, выбераешь нужный для тебя гипермаркет и следуешь инструкциям!\n
'''

def send_main_manu(): # клавиатура главного меню
    button1 = KeyboardButton("Пятёрочка")
    button2 = KeyboardButton("Магнит")
    button3 = KeyboardButton("/help")
    
    geo_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button1).add(button2).add(button3)
    return geo_kb


class GeneralState(StatesGroup): # основное состояние
    select_hyperstore = State()

#хендлер обработки команды старт и последующего вывода основной клавиатуры, 
# а так же проверки пользователя на админа и бан
async def start_command(message: types.Message, state: FSMContext): 
    if is_admin(message.from_id):
        async with state.proxy() as data:
            if 'last_msg' in data:
                await bot.delete_message(chat_id=message.chat.id, message_id=data['last_msg'])
            data['last_msg'] = await message.answer('Приветствую, Админ!', reply_markup=send_main_manu_admin())
            data['last_msg'] = data['last_msg']['message_id']
        await message.delete()
        await AdminState.admin_panel.set()
    elif is_admin(message.from_id) == 'ban':
            async with state.proxy() as data:
                if 'last_msg' in data:
                    await bot.delete_message(chat_id=message.chat.id, message_id=data['last_msg'])
                data['last_msg'] = await message.answer('доступ к боту заблокирован!')
                data['last_msg'] = data['last_msg']['message_id']
            await message.delete()
    else:
        async with state.proxy() as data:
            if 'last_msg' in data:
                await bot.delete_message(chat_id=message.chat.id, message_id=data['last_msg'])
            data['last_msg'] = await message.answer('Добро пожаловать в главное меню!', reply_markup=send_main_manu())
            data['last_msg'] = data['last_msg']['message_id']
        await message.delete()
        await GeneralState.select_hyperstore.set()

#хендлер обработки команды помощь
async def help_cmd(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id, message_id=data['last_msg'])
    msg = await message.answer(HELP_DESC, reply_markup=send_main_manu(), parse_mode='HTML')
    await message.delete()
    async with state.proxy() as data:
        data['last_msg'] = msg.message_id

#функция для регистрации объявленных хендлеров
def register_general_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command,commands=['start'], state='*')
    dp.register_message_handler(help_cmd,commands=['help'], state=GeneralState.select_hyperstore)
