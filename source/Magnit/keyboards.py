from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

def send_geoposition_replykb():
    
    button1 = KeyboardButton("🗺Отправить свою геолокацию🗺", request_location=True)
    button2 = KeyboardButton("Ввести данные вручную")
    
    geo_kb = ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True).add(button1).add(button2)
    return geo_kb

def select_category_kb():
    category_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True,keyboard=[[KeyboardButton('🍚бакалея🍝'),KeyboardButton('🍫кондитер🧁')],
                                                                                [KeyboardButton('🧼химия🧽'),KeyboardButton('🥤напитки🧃')],
                                                                                [KeyboardButton('☕️чай🍵'),KeyboardButton('🥶заморозка🥶')],
                                                                                [KeyboardButton('🥛молоко,яйца🍳'),KeyboardButton('🥩мясо🍗')],
                                                                                [KeyboardButton('🐟рыба🍤'),KeyboardButton('🍎овощи,фрукты🥦')],
                                                                                [KeyboardButton('другое'),KeyboardButton('назад')]])
    return category_kb



def next_or_stop_ikb():
    ib1 = InlineKeyboardButton('STOP',callback_data='stop')
    ib2 = InlineKeyboardButton('NEXT',callback_data='next')

    ikb = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[ib1,ib2]])
    return ikb


def send_select_store_ikb(store1, dist1, store2, dist2, store3, dist3):

    InlineButton1 = InlineKeyboardButton(text=f"1️⃣{store1.split(', ')[1]},{store1.split(', ')[2] if len(store1.split(', '))==3 else 'дом не указан'}д : {round(dist1,2)}km", callback_data='store1')
    InlineButton2 = InlineKeyboardButton(text=f"2️⃣{store2.split(', ')[1]},{store2.split(', ')[2] if len(store2.split(', '))==3 else 'дом не указан'}д : {round(dist2,2)}km", callback_data='store2')
    InlineButton3 = InlineKeyboardButton(text=f"3️⃣{store3.split(', ')[1]},{store3.split(', ')[2] if len(store3.split(', '))==3 else 'дом не указан'}д : {round(dist3,2)}km", callback_data='store3')

    inline_kb_for_select_store = InlineKeyboardMarkup(row_width=1,inline_keyboard=[[InlineButton1],
                                                                                   [InlineButton2],
                                                                                   [InlineButton3]])
    return inline_kb_for_select_store

def confirm_ikb():

    ibt1 = InlineKeyboardButton(text="✅",callback_data="yes")
    ibt2 = InlineKeyboardButton(text="🚫",callback_data="no")

    confirm_kb = InlineKeyboardMarkup(row_width=2,inline_keyboard=[[ibt1,ibt2]])
    return confirm_kb