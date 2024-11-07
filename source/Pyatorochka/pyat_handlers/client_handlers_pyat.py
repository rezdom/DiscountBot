from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from general_cient_handlers import GeneralState, send_main_manu

import sqlite3 as sq

from source.Magnit import keyboards
from source.Pyatorochka import config_pyat
from source.admin_handlers import AdminState, send_main_manu_admin
from source.general_config import is_admin

from create_bot import bot

from ScriptsForScrap.ScrapyPyat import ScrapyPyatBot, ScrapyPyatBot_HandMode

'''
объявляем хендлеры для режима парсинга магазина пятерочки
'''

class PyatState(StatesGroup): #статусы для парсинга пятерочки
    get_geo = State()
    select_store_state = State()
    confirm_store_state = State()
    send_discount = State()
    categoryes = State()
    input_address_state = State()

async def select_categor(category_name, code, disc): #функция, которая выбирает нужные нам продукты
    db_cards = sq.connect(config_pyat.file_path[0])
    cur_cards = db_cards.cursor()
    cur_cards.execute(f"SELECT {category_name} FROM id{code} WHERE discount >= {disc}")
    category_names_arr = cur_cards.fetchall()
    db_cards.close()
    return category_names_arr

async def create_5pos_message(arr_product, categor_name, data, message): #функция, которая создаёт первое сообщение для вывода первых 5 продуктов
    global products
    count = 0
    products = await select_categor(categor_name, data['store_code'], data['current_discount'])
    for item in products:
        if item[0] != None:
            arr_product.append(item[0])
            ind = products.index(item)
            for i in range(4):
                for j in range(ind+1, len(products)):
                    if products[j][0] != None:
                        arr_product.append(products[j][0])
                        ind = products.index(products[j])
                        break
    for card in products:
            if card[0] != None:
                count +=1
    if count <= 5:
        if count == 0:
            await message.answer(f"продуктов нет! выбери другую категорию!",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
        if count == 1:
            await message.answer(f"{'='*15}\n{arr_product[0]}",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
        elif count == 2:
            await message.answer(f"{'='*15}\n{arr_product[0]}\n{'='*15}\n{arr_product[1]}",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
        elif count == 3:
            await message.answer(f"{'='*15}\n{arr_product[0]}\n{'='*15}\n{arr_product[1]}\n{'='*15}\n{arr_product[2]}",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
        elif count == 4:
            await message.answer(f"{'='*15}\n{arr_product[0]}\n{'='*15}\n{arr_product[1]}\n{'='*15}\n{arr_product[2]}\n{'='*15}\n{arr_product[3]}",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
        else:
            await message.answer(f"{'='*15}\n{arr_product[0]}\n{'='*15}\n{arr_product[1]}\n{'='*15}\n{arr_product[2]}\n{'='*15}\n{arr_product[3]}\n{'='*15}\n{arr_product[4]}\n",parse_mode='HTML',
                                            reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
    else:
        await message.answer(f"{'='*15}\n{arr_product[0]}\n{'='*15}\n{arr_product[1]}\n{'='*15}\n{arr_product[2]}\n{'='*15}\n{arr_product[3]}\n{'='*15}\n{arr_product[4]}\n",parse_mode='HTML',
                                            reply_markup=keyboards.next_or_stop_ikb())
        return arr_product[4]

#хендлер, который обрабатывает апдейт
#для выбора отправки данных о местоположении

async def cmd_start(msg: types.Message, state: FSMContext):
    await msg.delete()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=msg.chat.id,message_id=data['last_msg'])
    mesg = await msg.answer('Выбери режим отправки данных, чтобы начать работу!',
               reply_markup=keyboards.send_geoposition_replykb())
    async with state.proxy() as data:
            data['last_msg'] = mesg.message_id
    await PyatState.get_geo.set()

async def cmd_input(msg: types.Message, state: FSMContext): #хендлер, который принимает местоположение в текстовом виде
    await msg.delete()
    async with state.proxy() as data:
            await bot.delete_message(chat_id=msg.chat.id,message_id=data['last_msg'])
            msg = await msg.answer('''Введи адрес где ты сейчас находишься в следующем стиле:\nМосковская область Москва Советская улица дом 1\n
                                   Или же если ваш город крупный(Москва,Санкт-Петербург и тд) то можно обойтись без упоминания области''')
            data['last_msg'] = msg.message_id
    await PyatState.input_address_state.set()

async def get_location(message: types.Message, state: FSMContext): #хендлер, который принимает местоположения в виде локации
    lat = message.location.latitude
    lon = message.location.longitude
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
        data['latitude'] = lat
        data['longitude'] = lon
    botPyat = ScrapyPyatBot(lat,lon)
    try:
        minimal_distance = await botPyat.get_stores(botPyat.latitude,botPyat.longitude)
        await message.delete()
        await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][0],
                                                                                                                     minimal_distance[0][0],
                                                                                                                     minimal_distance[1][1][0],
                                                                                                                     minimal_distance[1][0],
                                                                                                                     minimal_distance[2][1][0],
                                                                                                                     minimal_distance[2][0]))
        async with state.proxy() as data:
            data['store_code'] = (minimal_distance[0][1][1],minimal_distance[1][1][1],minimal_distance[2][1][1])
            data['lats'] = (minimal_distance[0][1][2],minimal_distance[1][1][2],minimal_distance[2][1][2])
            data['lons'] = (minimal_distance[0][1][3],minimal_distance[1][1][3],minimal_distance[2][1][3])
        await PyatState.select_store_state.set()
    except config_pyat.FindCityError as e:
        await message.delete()
        print('Магазинов пяторочки рядом не найдено!')
        await message.answer(text="Рядом с тобой не обнаружено магазинов :(\nПопробуй снова!")

async def get_location_hm(message: types.Message, state: FSMContext): #хендлер, который обрабатывает сообщение с местоположением через api яндекса и вывод 3 ближайших магазинов
    address_from_message = message.text
    botPyat_hm = ScrapyPyatBot_HandMode(address_from_message)
    coordinations_arr = botPyat_hm.get_crd_from_address(botPyat_hm.address)
    if coordinations_arr == "error":        
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
            msg = await message.answer("Видимо ты ввёл адрес неверно! Попробуй снова", reply=keyboards.send_geoposition_replykb())
            data['last_msg'] = msg.message_id
        await PyatState.get_geo.set()
        await message.delete()
        return 'ошибка в получении координат!'
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
            data['latitude'] = float(coordinations_arr[1])
            data['longitude'] = float(coordinations_arr[0])
    try:
        await message.delete()
        minimal_distance = await botPyat_hm.get_stores(data['latitude'],data['longitude'])
        await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][0],
                                                                                                                     minimal_distance[0][0],
                                                                                                                     minimal_distance[1][1][0],
                                                                                                                     minimal_distance[1][0],
                                                                                                                     minimal_distance[2][1][0],
                                                                                                                     minimal_distance[2][0]))
        async with state.proxy() as data:
            data['store_code'] = (minimal_distance[0][1][1],minimal_distance[1][1][1],minimal_distance[2][1][1])
            data['lats'] = (minimal_distance[0][1][2],minimal_distance[1][1][2],minimal_distance[2][1][2])
            data['lons'] = (minimal_distance[0][1][3],minimal_distance[1][1][3],minimal_distance[2][1][3])
        await PyatState.select_store_state.set()
    except config_pyat.FindCityError as e:
        await message.delete()
        print('Магазинов пяторочки рядом не найдено!')
        await message.answer(text="Рядом с тобой не обнаружено магазинов :(\nПопробуй снова!")


async def select_category(message: types.Message, state:FSMContext): #формирование карточек с 5ю продуктами
    global products, count_for_cards
    count_for_cards = 5
    arr_product = []
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
        if message.text == '🍚бакалея🍝':
            data['last_card'] = await create_5pos_message(arr_product, 'bakal_souse', data, message)

        elif message.text == '🍫кондитер🧁':
            data['last_card'] = await create_5pos_message(arr_product, 'konditer', data, message)
        
        elif message.text == '🧼химия🧽':
            data['last_card'] = await create_5pos_message(arr_product, 'him', data, message)
        
        elif message.text == '🥤напитки🧃':
            data['last_card'] = await create_5pos_message(arr_product, 'water', data, message)

        elif message.text == '☕️чай🍵':
            data['last_card'] = await create_5pos_message(arr_product, 'tea_coffe', data, message)

        elif message.text == '🥶заморозка🥶':
            data['last_card'] = await create_5pos_message(arr_product, 'freeze', data, message)

        elif message.text == '🥛молоко,яйца🍳':
            data['last_card'] = await create_5pos_message(arr_product, 'milk_eggs', data, message)

        elif message.text == '🥩мясо🍗':
            data['last_card'] = await create_5pos_message(arr_product, 'meat', data, message)

        elif message.text == '🐟рыба🍤': 
            data['last_card'] = await create_5pos_message(arr_product, 'fish', data, message)

        elif message.text == '🍎овощи,фрукты🥦':
            data['last_card'] = await create_5pos_message(arr_product, 'fruts_veg', data, message)

        elif message.text == 'другое':
            data['last_card'] = await create_5pos_message(arr_product, 'other', data, message)   

        else:
            msg = await message.answer('вернулись в главное меню!',
                                    reply_markup=send_main_manu() if not is_admin(message.from_id) else send_main_manu_admin())
            async with state.proxy() as data:
                data['last_msg'] = msg.message_id
            if is_admin(message.from_id):
                await AdminState.admin_panel.set()
            else:
                await GeneralState.select_hyperstore.set()
        await message.delete()





async def selected_store(callback: types.Message, state: FSMContext): #хендлер, который обрабатывает апдейт с выбранной ближайшей точкой
    if callback.data == 'store1':
        async with state.proxy() as data:
            data['store_code'] = data['store_code'][0]
            data['lats'] = data['lats'][0]
            data['lons'] = data['lons'][0]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['lats']),longitude=float(data['lons']))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    elif callback.data == 'store2':
        async with state.proxy() as data:
            data['store_code'] = data['store_code'][1]
            data['lats'] = data['lats'][1]
            data['lons'] = data['lons'][1]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['lats']),longitude=float(data['lons']))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    elif callback.data == 'store3':
        async with state.proxy() as data:
            data['store_code'] = data['store_code'][2]
            data['lats'] = data['lats'][2]
            data['lons'] = data['lons'][2]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['lats']),longitude=float(data['lons']))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    await PyatState.confirm_store_state.set()


async def send_discount(callback: types.Message, state: FSMContext): #подтверждение магазина и принимаем нужную скидку
    if callback.data == 'yes':
        async with state.proxy() as data:
            botPyat = ScrapyPyatBot(data['latitude'],data['longitude'])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg'])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg']+1)
        msg_id = await bot.send_message(chat_id=callback.from_user.id,text=f"Сканирую страницу 1")
        msg_id = msg_id.message_id
        try:
            await botPyat.get_cards(data['store_code'],botPyat, bot, callback, msg_id)
            await bot.delete_message(chat_id=callback.from_user.id, message_id=msg_id)
            msg = await bot.send_message(chat_id=callback.from_user.id,text=f"Введи размер скидки --> от 0% до 90%(Вводи только число)", reply_markup=ReplyKeyboardRemove())
            async with state.proxy() as data:    
                data['last_msg'] = msg.message_id
            await PyatState.send_discount.set()
        except config_pyat.NotProductsError:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=msg_id)
            msg = await bot.send_message(chat_id=callback.from_user.id,text=f"На сайте отсутсвуют товары! Попробуй позже\nВернулись в главное меню",reply_markup=send_main_manu() if not is_admin(callback.from_id) else send_main_manu_admin())
            async with state.proxy() as data:    
                data['last_msg'] = msg.message_id
            if is_admin(callback.from_id):
                await AdminState.admin_panel.set()
            else:
                await GeneralState.select_hyperstore.set()
    elif callback.data == 'no':
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg'])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg']+1)
        async with state.proxy() as data:
            data['last_msg'] = await bot.send_message(chat_id=callback.from_user.id, text='Окей, попробуй ещё раз!',reply_markup=keyboards.send_geoposition_replykb())
            data['last_msg'] = data['last_msg']['message_id']
        await PyatState.get_geo.set()


async def confirm_store(message: types.Message, state: FSMContext): #вывод клавиатуры с категориями
    if int(message.text) >= 0 and int(message.text) <= 90:
        async with state.proxy() as data:
            data['current_discount'] = int(message.text)   
            await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg']) 
            msg = await bot.send_message(chat_id=message.from_user.id,text=f"Выбери категорию {data['store_code']}", reply_markup=keyboards.select_category_kb())
            data['last_msg'] = msg.message_id
        await PyatState.categoryes.set()
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
            msg = await bot.send_message(chat_id=message.from_user.id, text='Ты ввёл не то число, попробуй ещё раз!',reply_markup=keyboards.send_geoposition_replykb())
            data['last_msg'] = msg.message_id
    await message.delete()


async def callback_stop_next(callback: types.CallbackQuery, state:FSMContext): #хендлер, который обрабатывает callback, когда листаем карточки с товаром
    if callback.data == 'next':
        global count_for_cards
        count = 0
        arr_products = []
        count_for_cards += 5
        for card in products:
            if card[0] != None:
                count +=1
        async with state.proxy() as data:
            if count_for_cards <= count:
                ind = products.index((data['last_card'],))
                for i in range(5):
                    for j in range(ind+1,len(products)):
                        if products[j][0] != None:
                            arr_products.append(products[j][0])
                            ind = products.index((products[j][0],))
                            break
                await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n{'='*15}\n{arr_products[1]}\n{'='*15}\n{arr_products[2]}\n{'='*15}\n{arr_products[3]}\n{'='*15}\n{arr_products[4]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=keyboards.next_or_stop_ikb())
                data['last_card'] = arr_products[4]
            else:
                ind = products.index((data['last_card'],))
                for j in range(ind+1,len(products)):
                    if products[j][0] != None:
                        arr_products.append(products[j][0])
                if len(arr_products) == 1:
                    await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
                elif len(arr_products) == 2:
                    await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n{'='*15}\n{arr_products[1]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
                elif len(arr_products) == 3:
                    await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n{'='*15}\n{arr_products[1]}\n{'='*15}\n{arr_products[2]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
                elif len(arr_products) == 4:
                    await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n{'='*15}\n{arr_products[1]}\n{'='*15}\n{arr_products[2]}\n{'='*15}\n{arr_products[3]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
                else:
                    await bot.edit_message_text(chat_id=callback.from_user.id,text=f"{'='*15}\n{arr_products[0]}\n{'='*15}\n{arr_products[1]}\n{'='*15}\n{arr_products[2]}\n{'='*15}\n{arr_products[3]}\n{'='*15}\n{arr_products[4]}\n",parse_mode='HTML',
                                            message_id=callback.message.message_id,reply_markup=InlineKeyboardMarkup(row_width=2,inline_keyboard=[[InlineKeyboardButton('STOP',callback_data='stop')]]))
    else:
        await bot.delete_message(chat_id=callback.from_user.id,message_id=callback.message.message_id)
        msg = await bot.send_message(chat_id=callback.from_user.id, text='выбери новою категорию', reply_markup=keyboards.select_category_kb())
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id



def register_pyat_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start,Text(equals='Пятёрочка'), state=[GeneralState.select_hyperstore, AdminState.admin_panel])
    dp.register_message_handler(get_location,content_types=['location'], state=PyatState.get_geo)
    dp.register_message_handler(select_category, Text(equals=['🍚бакалея🍝', '🍫кондитер🧁', '🧼химия🧽', '🥤напитки🧃', '☕️чай🍵', '🥶заморозка🥶', '🥛молоко,яйца🍳', '🥩мясо🍗', '🐟рыба🍤', '🍎овощи,фрукты🥦', 'другое', 'назад']), state=PyatState.categoryes)
    dp.register_message_handler(cmd_input, Text(equals='Ввести данные вручную'), state=PyatState.get_geo)
    dp.register_message_handler(get_location_hm, state=PyatState.input_address_state, content_types=['text'])
    dp.register_message_handler(confirm_store, state=PyatState.send_discount, content_types=['text'])

    dp.register_callback_query_handler(selected_store,state=PyatState.select_store_state)
    dp.register_callback_query_handler(send_discount,state=PyatState.confirm_store_state)
    dp.register_callback_query_handler(callback_stop_next,state=PyatState.categoryes)