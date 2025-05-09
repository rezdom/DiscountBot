from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.filters import StateFilter

from src.bot.utils.states import MagnitStates, GeneralState, user_products
from src.database.utils.enum_models import MarketGroups, ProductTypes
from src.bot.keyboards import general_keyboards as gk
from src.scraping.magnit import get_stores, get_data
from src.bot.utils.big_info import INPUT_ADDRESS
from src.scraping.geo import get_address_info
from src.database.orm import AsyncProductOrm, AsyncSklepOrm
from src.database.db_models import Product

router = Router()

def format_page(products: list[Product], offset: int, per_page = 5):
    visible_products = products[offset:offset+per_page]

    if not visible_products:
        return ("Продуктов нет на этой странице.", gk.get_next_or_back(offset, len(products), per_page))
    
    message_text = "\n".join(
        f"{'='*15}\n{product.name}\nСкидка: -{product.discount}%\nСтарая цена: <s>{product.price / 100:.2f}</s>\n Новая цена: <b>{((product.price / 100)*(1-product.discount/100)):.2f}</b>" for product in visible_products
    )
    return message_text, gk.get_next_or_back(offset, len(products), per_page)


@router.message(F.text=='🔴МАГНИТ', StateFilter(GeneralState.start))
async def get_address(message: Message, state: FSMContext):
    await state.set_state(MagnitStates.waiting_input_address)
    await state.update_data(store_type=MarketGroups.MAGNIT)
    await message.answer("Выбери режим отправки данных, чтобы начать работу!",
                   reply_markup=gk.get_location)

@router.message(F.location, StateFilter(MagnitStates.waiting_input_address))
async def get_stores_location(message: Message, state: FSMContext):
    location = message.location
    stores = await get_stores(lat=location.latitude, long=location.longitude)
    if stores:
        await state.set_state(MagnitStates.select_store)
        await state.update_data(stores=stores)
        await message.answer("Выбери подходящий тебе магазин:",
                            reply_markup=gk.get_select_store(*stores))
    else:
        await state.set_data(default_state)
        await state.set_data(GeneralState.start)
        await message.answer(f"Проблема получения данных о магазине магнита (Проблема парсинга или рядом с тобой нет магазинов).\n"\
                             "Попробуй позже!\n"\
                                "Теперь ты в главном меню!", reply_markup=gk.main_menu_client)

@router.message(F.text=="Ввести данные вручную", StateFilter(MagnitStates.waiting_input_address))
async def input_address(message: Message, state: FSMContext):
    await state.set_state(MagnitStates.input_address)
    await message.answer(INPUT_ADDRESS, parse_mode="HTML")

@router.message(F.text=="Главное меню", StateFilter(MagnitStates.waiting_input_address))
async def back_to_main_menu(message: Message, state: FSMContext):
    await state.set_state(default_state)
    await state.set_state(GeneralState.start)
    await message.answer("Добро пожаловать в главное меню! Выбери магазин:",
                         reply_markup=gk.main_menu_client)

@router.message(F.text, StateFilter(MagnitStates.input_address))
async def get_stores_address(message: Message, state: FSMContext):
    location = await get_address_info(message.text)
    if location:
        stores = await get_stores(lat=location.latitude, long=location.longitude)
        if stores:
            await state.set_state(MagnitStates.select_store)
            await state.update_data(stores=stores)
            await message.answer("Выбери подходящий тебе магазин:",
                                reply_markup=gk.get_select_store(*stores))
        else:
            await state.set_data(default_state)
            await state.set_data(GeneralState.start)
            await message.answer(f"Проблема получения данных о магазине магнита (Проблема парсинга или рядом с тобой нет магазинов).\n"\
                                "Попробуй позже!\n"\
                                    "Теперь ты в главном меню!", reply_markup=gk.main_menu_client)
    else:
        await message.answer(f"Видимо ты ввел что-то не так, попробуй еще раз!")


@router.callback_query(StateFilter(MagnitStates.select_store), F.data.startswith("store"))
async def get_store(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("Идет выгрузка данных, ожидайте...")
    data = await state.get_data()
    store = data.get("stores")[int(callback.data[-1])]
    await state.set_state(MagnitStates.input_discount)
    await state.update_data(select_store=store)
    sklep = await AsyncSklepOrm.get_sklep(store[0])
    if not sklep or (await AsyncSklepOrm.get_update_sklep(store[1])):
        if (await AsyncSklepOrm.get_update_sklep(store[1])):
            await AsyncSklepOrm.del_sklep(store[1])
        sklep = await AsyncSklepOrm.add_sklep(data.get("store_type"), store[1], store[0])
        await get_data(sklep.id, sklep.shop_id)
    await state.update_data(sklep_id=sklep.id)
    await callback.message.edit_text(f"Вы выбрали: {store[0]}\n"\
                                "Введи скидку от 0% до 100%(Просто число)\n" \
                                "Будут выбраны товары от n% до 100%")

@router.message(StateFilter(MagnitStates.input_discount), F.text)
async def get_discount(message: Message, state: FSMContext):
    try:
        discount = int(message.text)
        if not (0 <= discount <= 100):
            raise ValueError  # Принудительно вызовем ошибку, если число вне диапазона
        # Всё в порядке, сохраняем скидку и идем дальше
        await state.update_data(discount=discount)
        await state.set_state(MagnitStates.select_type)
        await message.answer("Теперь выбери тип товара:", reply_markup=gk.product_types)
    except ValueError:
        # Если введено не число или число вне допустимого диапазона
        await message.answer("Пожалуйста, введи **число от 0 до 100**.\n"
                             "Например: `25` для 25% скидки.\n"
                             "Попробуй ещё раз:")

@router.callback_query(F.data.in_([str(item.value) for item in ProductTypes]), StateFilter(MagnitStates.select_type))
async def load_product_list(callback: CallbackQuery, state:FSMContext):
    product_type = ProductTypes(int(callback.data))
    await state.update_data(product_type=product_type)
    await state.set_state(MagnitStates.pages_list)
    data = await state.get_data()
    user_products[callback.message.from_user.id] = await AsyncProductOrm.get_products(data.get("sklep_id"), data.get("product_type"), data.get("discount"))

    offset = 0
    message_text, reply_markup = format_page(user_products[callback.message.from_user.id], offset)

    await state.update_data(offset=offset)
    await callback.message.edit_text(message_text, parse_mode="HTML", reply_markup=reply_markup)

@router.callback_query(F.data.in_(["back"]), StateFilter(MagnitStates.select_type))
async def get_product_list(callback: CallbackQuery, state:FSMContext):
    await state.set_state(default_state)
    user_products.pop(callback.message.from_user.id, None)
    await state.set_state(GeneralState.start)
    await callback.message.answer("Добро пожаловать в главное меню! Выбери магазин:",
                         reply_markup=gk.main_menu_client)

@router.callback_query(F.data.in_(["next", "back"]), StateFilter(MagnitStates.pages_list))
async def paginate_products(callback: CallbackQuery, state: FSMContext):
    user_id = callback.message.from_user.id
    data = await state.get_data()

    offset = data.get("offset")
    if callback.data == "next":
        offset += 5
    elif callback.data == "back":
        offset = max(0, offset - 5)
    products = user_products.get(user_id, [])
    message_text, reply_markup = format_page(products, offset)

    await state.update_data(offset=offset)

    await callback.message.edit_text(message_text, parse_mode="HTML", reply_markup=reply_markup)

@router.callback_query(F.data.in_(["menu"]), StateFilter(MagnitStates.pages_list))
async def to_select_type(callback: CallbackQuery, state: FSMContext):
    user_products.pop(callback.message.from_user.id, None)
    await state.set_state(MagnitStates.select_type)
    await callback.message.edit_text("Теперь выбери тип товара:", reply_markup=gk.product_types)