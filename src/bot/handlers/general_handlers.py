from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.bot.keyboards.general_keyboards as general_kb
from src.bot.utils.states import GeneralState, user_products
from src.database.orm import AsyncUserOrm, AsyncReportOrm
from src.database.utils.enum_models import UserRole
from src.bot.utils.config import ADMIN_LIST

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(default_state)
    user_products.pop(message.from_user.id, None)
    user = await AsyncUserOrm.get_user(message.from_user.id)
    if not user: user = await AsyncUserOrm.add_user(message.from_user.id, message.from_user.username)
    if user.telegram_id in ADMIN_LIST and not (user.role == UserRole.ADMIN): user = await AsyncUserOrm.to_admin(message.from_user.id)
    await state.set_state(GeneralState.start)
    await message.answer("Добро пожаловать в главное меню! Выбери магазин:",
                         reply_markup=general_kb.main_menu_client)

@router.message(Command("adm"), StateFilter(GeneralState.start))
async def cmd_adm(message: Message, state: FSMContext):
    user = await AsyncUserOrm.get_user(message.from_user.id)
    if user.role == UserRole.ADMIN:
        await state.set_state(GeneralState.admin)
        await message.answer("Добро пожаловать в панель администратора! Выбери инструмент:",
                         reply_markup=general_kb.adm_kb)

@router.message(F.text=="Report", StateFilter(GeneralState.start))
async def create_report(message: Message, state: FSMContext):
    await state.set_state(GeneralState.create_report)
    await message.answer("Распишите свою проблему как можно подробнее (Не более 1024 символов)")

@router.message(F.text, StateFilter(GeneralState.create_report))
async def input_report(message: Message, state: FSMContext):
    user = await AsyncUserOrm.get_user(message.from_user.id)
    if len(message.text) < 1024:
        report = await AsyncReportOrm.add_report(user.id, user.telegram_id, message.text)
        await state.set_state(default_state)
        await state.set_state(GeneralState.start)
        await message.answer(f"Ваше обращение создано! Report №{report.id}\nДобро пожаловать в главное меню! Выбери магазин:",
                             reply_markup=general_kb.main_menu_client)
    elif len(message.text) == 0:
        await message.answer("Нельзя отправлять пустое обращение, попробуй еще раз!")
    else:
        await message.answer("Ваше обращение превышает ограничение в 1024 символа, попробуйте еще раз!")