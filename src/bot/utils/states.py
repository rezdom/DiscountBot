from aiogram.fsm.state import State, StatesGroup


user_products: dict[int, list] = {}

class GeneralState(StatesGroup):
    start = State()
    admin = State()
    create_report = State()

class AdminStates(StatesGroup):
    input_admin = State()
    input_ban = State()
    input_unban = State()

class MagnitStates(StatesGroup):
    waiting_input_address = State()
    input_address = State()
    select_store = State()
    input_discount = State()
    select_type = State()
    pages_list = State()

class PyatorochkaState(StatesGroup):
    waiting_input_address = State()
    input_address = State()
    input_discount = State()
    select_type = State()
    pages_list = State()