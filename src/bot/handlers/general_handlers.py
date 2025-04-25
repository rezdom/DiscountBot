from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.bot.keyboards.general_keyboards as general_kb
from src.bot.utils.states import MagnitStates, GeneralState, user_products

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(default_state)
    user_products.pop(message.from_user.id, None)
    await state.set_state(GeneralState.start)
    await message.answer("Добро пожаловать в главное меню! Выбери магазин:",
                         reply_markup=general_kb.main_menu_client)


    