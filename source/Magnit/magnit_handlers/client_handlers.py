import sys, os
sys.path.append(os.path.abspath('../BotParsSale'))

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import sqlite3 as sq

from source.Magnit import keyboards
from source.Magnit import config
from source.admin_handlers import AdminState, send_main_manu_admin
from source.general_config import is_admin

from general_cient_handlers import GeneralState, send_main_manu

from create_bot import bot

from ScriptsForScrap.ScrapyMagnit import ScrapyMagnitBot, ScrapyMagnitBot_HandMode

class Test(StatesGroup):
    get_geo = State()
    select_store_state = State()
    confirm_store_state = State()
    select_discount = State()
    categoryes = State()
    input_address_state = State()

async def select_categor(category_name, file_ID, disc): 
    db_cards = sq.connect(config.file_path[2])
    cur_cards = db_cards.cursor()
    cur_cards.execute(f"SELECT {category_name} FROM id_{file_ID} WHERE discount >= {disc}")
    category_names_arr = cur_cards.fetchall()
    db_cards.close()
    return category_names_arr

async def create_5pos_message(arr_product, categor_name, data, message):
    global products
    count = 0
    products = await select_categor(categor_name, data['fileID'], data['current_discount'])
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
        elif count == 1:
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


async def cmd_start(msg: types.Message, state: FSMContext):
    await msg.delete()
    async with state.proxy() as data:
        await bot.delete_message(chat_id=msg.chat.id,message_id=data['last_msg'])
    msg = await msg.answer('Выбери режим отправки данных, чтобы начать работу!',
               reply_markup=keyboards.send_geoposition_replykb())
    async with state.proxy() as data:
            data['last_msg'] = msg.message_id
    await Test.get_geo.set()

async def cmd_input(msg: types.Message, state: FSMContext):
    await msg.delete()
    msg = await msg.answer('''Введи адрес где ты сейчас находишься в следующем стиле:\nМосковская область Москва Советская улица дом 1\n
                                   Или же если ваш город крупный(Москва,Санкт-Петербург и тд) то можно обойтись без упоминания области''')
    async with state.proxy() as data:
            await bot.delete_message(chat_id=msg.chat.id,message_id=data['last_msg'])
            data['last_msg'] = msg.message_id
    await Test.input_address_state.set()


async def get_location(message: types.Message, state: FSMContext):
    lat = message.location.latitude
    lon = message.location.longitude
    async with state.proxy() as data:
        await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
        data['latitude'] = lat
        data['longitude'] = lon
    botMagnit = ScrapyMagnitBot(lat,lon)
    try:
        coordinations = botMagnit.get_address_from_crd(botMagnit.latitude,botMagnit.longitude)
        current_city = botMagnit.find_city(coordinations[0],coordinations[1], botMagnit)
        async with state.proxy() as data:
            data['current_city'] = current_city[0]
        botMagnit.input_cities_table(current_city[0],current_city[1],current_city[2],botMagnit)
        minimal_distance = botMagnit.find_nearest_store(current_city[0],botMagnit.latitude,botMagnit.longitude, botMagnit)
        await message.delete()
        await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][1],
                                                                                                                     minimal_distance[0][1][0],
                                                                                                                     minimal_distance[1][1][1],
                                                                                                                     minimal_distance[1][1][0],
                                                                                                                     minimal_distance[2][1][1],
                                                                                                                     minimal_distance[2][1][0]))
        async with state.proxy() as data:
            data['coordinations'] = (minimal_distance[0][0],minimal_distance[1][0],minimal_distance[2][0])
        await Test.select_store_state.set()
    except config.FindCityError:
        await message.delete()
        print('Город не найден')
        await message.answer(text="Рядом с тобой не обнаружен город :(\nПопробуй снова!")
    except config.ActualError as ae:
        await message.delete()
        print('Информация актуальна')
        minimal_distance = botMagnit.find_nearest_store(ae.args[1],botMagnit.latitude,botMagnit.longitude, botMagnit)
        async with state.proxy() as data:
            data['current_city'] = ae.args[1]
        await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][1],
                                                                                                                     minimal_distance[0][1][0],
                                                                                                                     minimal_distance[1][1][1],
                                                                                                                     minimal_distance[1][1][0],
                                                                                                                     minimal_distance[2][1][1],
                                                                                                                     minimal_distance[2][1][0]))
        async with state.proxy() as data:
            data['coordinations'] = (minimal_distance[0][0],minimal_distance[1][0],minimal_distance[2][0])
        botMagnit.db_for_cities.close()
        botMagnit.db_for_stores.close()
        botMagnit.db_for_cards.close()
        await Test.select_store_state.set()


async def get_location_hm(message: types.Message, state: FSMContext):
    address_from_message = message.text
    botMagnit_hm = ScrapyMagnitBot_HandMode(address_from_message)
    coordinations_arr = botMagnit_hm.get_crd_from_address(botMagnit_hm.address)
    if coordinations_arr == "error":
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
        msg = await message.answer("Видимо ты ввёл адрес неверно! Попробуй снова", reply=keyboards.send_geoposition_replykb())
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await Test.get_geo.set()
        return 'ошибка в получении координат!'
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.chat.id,message_id=data['last_msg'])
            data['latitude'] = float(coordinations_arr[1])
            data['longitude'] = float(coordinations_arr[0])
        try:
            coordinations = botMagnit_hm.get_address_from_crd(data['latitude'],data['longitude'])
            if len(coordinations) == 1:
                current_city = botMagnit_hm.find_big_city(coordinations[0], botMagnit_hm)
            else:
                current_city = botMagnit_hm.find_city(coordinations[0],coordinations[1], botMagnit_hm)
            async with state.proxy() as data:
                data['current_city'] = current_city[0]
            botMagnit_hm.input_cities_table(current_city[0],current_city[1],current_city[2],botMagnit_hm)
            minimal_distance = botMagnit_hm.find_nearest_store(current_city[0],data['latitude'],data['longitude'], botMagnit_hm)
            await message.delete()
            await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][1],
                                                                                                                        minimal_distance[0][1][0],
                                                                                                                        minimal_distance[1][1][1],
                                                                                                                        minimal_distance[1][1][0],
                                                                                                                        minimal_distance[2][1][1],
                                                                                                                        minimal_distance[2][1][0]))
            async with state.proxy() as data:
                data['coordinations'] = (minimal_distance[0][0],minimal_distance[1][0],minimal_distance[2][0])
            await Test.select_store_state.set()
        except config.FindCityError:
            await message.delete()
            print('Город не найден')
            await message.answer(text="Рядом с тобой не обнаружен город :(\nПопробуй снова!")
            await Test.get_geo.set()
        except config.ActualError as ae:
            await message.delete()
            print('Информация актуальна')
            minimal_distance = botMagnit_hm.find_nearest_store(ae.args[1],data['latitude'],data['longitude'], botMagnit_hm)
            async with state.proxy() as data:
                data['current_city'] = ae.args[1]
            await message.answer(text="Выбери подходящий для тебя магазин!",reply_markup=keyboards.send_select_store_ikb(minimal_distance[0][1][1],
                                                                                                                        minimal_distance[0][1][0],
                                                                                                                        minimal_distance[1][1][1],
                                                                                                                        minimal_distance[1][1][0],
                                                                                                                        minimal_distance[2][1][1],
                                                                                                                        minimal_distance[2][1][0]))
            async with state.proxy() as data:
                data['coordinations'] = (minimal_distance[0][0],minimal_distance[1][0],minimal_distance[2][0])
            botMagnit_hm.db_for_cities.close()
            botMagnit_hm.db_for_stores.close()
            botMagnit_hm.db_for_cards.close()
            await Test.select_store_state.set()



async def select_category(message: types.Message, state:FSMContext):
    global count_for_cards
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
    



async def selected_store(callback: types.Message, state: FSMContext):
    if callback.data == 'store1':
        async with state.proxy() as data:
            data['coordinations'] = data['coordinations'][0]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['coordinations'][0]),longitude=float(data['coordinations'][1]))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    elif callback.data == 'store2':
        async with state.proxy() as data:
            data['coordinations'] = data['coordinations'][1]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['coordinations'][0]),longitude=float(data['coordinations'][1]))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    elif callback.data == 'store3':
        async with state.proxy() as data:
            data['coordinations'] = data['coordinations'][2]
        await bot.delete_message(chat_id=callback.from_user.id, message_id=callback.message.message_id)
        msg = await bot.send_location(chat_id=callback.from_user.id,latitude=float(data['coordinations'][0]),longitude=float(data['coordinations'][1]))
        async with state.proxy() as data:
            data['last_msg'] = msg.message_id
        await bot.send_message(chat_id=callback.from_user.id, text="Тебе подходит этот магазин?", reply_markup=keyboards.confirm_ikb())
    await Test.confirm_store_state.set()


async def send_discount(callback: types.Message, state: FSMContext):
    if callback.data == 'yes':
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg'])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg']+1)
            msg = await bot.send_message(chat_id=callback.from_user.id,text=f"Введи размер скидки --> от 0% до 90%(Вводи только число)", reply_markup=ReplyKeyboardRemove())
            data['last_msg'] = msg.message_id
        await Test.select_discount.set()
    elif callback.data == 'no':
        async with state.proxy() as data:
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg'])
            await bot.delete_message(chat_id=callback.from_user.id, message_id=data['last_msg']+1)
            msg = await bot.send_message(chat_id=callback.from_user.id, text='Окей, попробуй ещё раз!',reply_markup=keyboards.send_geoposition_replykb())
            data['last_msg'] = msg.message_id
        await Test.get_geo.set()

async def confirm_store(message: types.Message, state: FSMContext):
    if int(message.text) >= 0 and int(message.text) <= 90:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
            data['current_discount'] = int(message.text)
            botMagnit = ScrapyMagnitBot(data['latitude'],data['longitude'])
        storeID, address = botMagnit.selected_city(data['coordinations'],data['current_city'],botMagnit)
        async with state.proxy() as data:
            data['fileID'] = await botMagnit.get_product_cards(storeID, address, botMagnit)
            msg = await bot.send_message(chat_id=message.from_user.id,text=f"Выбери категорию {data['fileID']}", reply_markup=keyboards.select_category_kb())
            data['last_msg'] = msg.message_id
        await bot.delete_message(chat_id=message.from_user.id,message_id=message.message_id)
        botMagnit.db_for_cities.close()
        botMagnit.db_for_stores.close()
        botMagnit.db_for_cards.close()
        await Test.categoryes.set()
    else:
        async with state.proxy() as data:
            await bot.delete_message(chat_id=message.from_user.id, message_id=data['last_msg'])
            msg = await bot.send_message(chat_id=message.from_user.id, text='Ты ввёл не то число, попробуй ещё раз!',reply_markup=keyboards.send_geoposition_replykb())
            data['last_msg'] = msg.message_id


async def callback_stop_next(callback: types.CallbackQuery, state:FSMContext):
    if callback.data == 'next':
        global count_for_cards
        arr_products = []
        count = 0
        count_for_cards += 5
        for card in products:
            if card[0] != None:
                count +=1
        async with state.proxy() as data:
            if count_for_cards < count:
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



def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(cmd_start,Text(equals='Магнит'), state=[GeneralState.select_hyperstore, AdminState.admin_panel])
    dp.register_message_handler(get_location,content_types=['location'], state=Test.get_geo)
    dp.register_message_handler(select_category, Text(equals=['🍚бакалея🍝', '🍫кондитер🧁', '🧼химия🧽', '🥤напитки🧃', '☕️чай🍵', '🥶заморозка🥶', '🥛молоко,яйца🍳', '🥩мясо🍗', '🐟рыба🍤', '🍎овощи,фрукты🥦', 'другое', 'назад']), state=Test.categoryes)
    dp.register_message_handler(cmd_input, Text(equals='Ввести данные вручную'), state=Test.get_geo)
    dp.register_message_handler(get_location_hm, state=Test.input_address_state, content_types=['text'])
    dp.register_message_handler(confirm_store, state=Test.select_discount, content_types=['text'])

    dp.register_callback_query_handler(selected_store,state=Test.select_store_state)
    dp.register_callback_query_handler(send_discount,state=Test.confirm_store_state)
    dp.register_callback_query_handler(callback_stop_next,state=Test.categoryes)