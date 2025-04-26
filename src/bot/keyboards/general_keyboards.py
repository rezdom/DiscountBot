from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.utils.enum_models import ProductTypes

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

product_types = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🍚 Бакалея 🍝', callback_data=str(ProductTypes.GROCERY_SAUCES.value))],
    [InlineKeyboardButton(text='🍫 Сладости 🧁', callback_data=str(ProductTypes.SWEETS.value))],
    [InlineKeyboardButton(text='🧼 Химия 🧽', callback_data=str(ProductTypes.CHEMISTRY.value))],
    [InlineKeyboardButton(text='🥤 Напитки 🧃', callback_data=str(ProductTypes.DRINKS.value))],
    [InlineKeyboardButton(text='☕️ Чай/Кофе 🍵', callback_data=str(ProductTypes.TEA_COFFEE.value))],
    [InlineKeyboardButton(text='🍟 Чипсы/Орехи 🍟', callback_data=str(ProductTypes.SNACKS_NUTS.value))],
    [InlineKeyboardButton(text='🥛 Молоко/Яйца 🍳', callback_data=str(ProductTypes.DAIRY_EGGS.value))],
    [InlineKeyboardButton(text='🥩 Мясо 🍗', callback_data=str(ProductTypes.MEAT.value))],
    [InlineKeyboardButton(text='🐟 Рыба 🍤', callback_data=str(ProductTypes.FISH.value))],
    [InlineKeyboardButton(text='🍎 Овощи/Фрукты 🥦', callback_data=str(ProductTypes.VEGETABLES_FRUITS.value))],
    [InlineKeyboardButton(text='🍞 Выпечка 🥧', callback_data=str(ProductTypes.BAKERY.value))],
    [InlineKeyboardButton(text='🔞 Алкоголь 🍺', callback_data=str(ProductTypes.ALCO.value))],
    [InlineKeyboardButton(text='🧺 Другое', callback_data=str(ProductTypes.OTHER.value))],
    [InlineKeyboardButton(text='🏠 Главное меню', callback_data="back")]
])


main_menu_client = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="🔴МАГНИТ")],
    [KeyboardButton(text="5️⃣ПЯТЕРОЧКА")],
    [KeyboardButton(text="Report")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери пункт меню..."
)
adm_kb = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="Назначить админом")],
    [KeyboardButton(text="Бан"), KeyboardButton(text="Разбан")],
    [KeyboardButton(text="Обращения пользователей")],
    [KeyboardButton(text="Главное меню")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери пункт меню..."
)

get_location = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📍 Отправить свою геолокацию", request_location=True)],
        [KeyboardButton(text="Ввести данные вручную")],
        [KeyboardButton(text = "Главное меню")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder="Выбери пункт меню..."
)

def get_select_store(store1: tuple, store2: tuple, store3:tuple):
    select_store = InlineKeyboardMarkup(
        inline_keyboard=[
        [InlineKeyboardButton(text=f"{store1[2]}km: {','.join(store1[0].split(',')[-3:])}", callback_data="store_0")],
        [InlineKeyboardButton(text=f"{store2[2]}km: {','.join(store2[0].split(',')[-3:])}", callback_data="store_1")],
        [InlineKeyboardButton(text=f"{store3[2]}km: {','.join(store3[0].split(',')[-3:])}", callback_data="store_2")],
        ]
    )
    return select_store

def get_next_or_back(current_offset: int, total_items: int, items_per_page: int = 5):
    keyboard = []
    pagination_buttons = []
    if current_offset > 0:
        pagination_buttons.append(InlineKeyboardButton(text="⬅️Назад", callback_data="back"))
    if current_offset + items_per_page < total_items:
        pagination_buttons.append(InlineKeyboardButton(text="➡️Далее", callback_data="next"))
    
    keyboard.append(pagination_buttons)
    keyboard.append([InlineKeyboardButton(text="Меню", callback_data="menu")])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)