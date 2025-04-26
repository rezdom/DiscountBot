from aiogram import Router, F
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state

import src.bot.keyboards.general_keyboards as general_kb
from src.bot.utils.states import GeneralState, AdminStates
from src.database.orm import AsyncUserOrm, AsyncReportOrm

router = Router()

@router.message(StateFilter(GeneralState.admin), F.text=="Назначить админом")
async def set_admin_role(message:Message, state: FSMContext):
    await state.set_state(AdminStates.input_admin)
    await message.answer("Введи id пользователья, которого хочешь назначить админом")

@router.message(StateFilter(AdminStates.input_admin), F.text)
async def set_admin_role(message:Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(f"Введи id пользователя!", reply_markup=general_kb.adm_kb)
        return
    await state.set_state(GeneralState.admin)
    user = await AsyncUserOrm.to_admin(int(message.text))
    if user:
        await message.answer(f"Пользователь {user.telegram_username}: {user.telegram_id} назанчен админом!", reply_markup=general_kb.adm_kb)
    else:
        await message.answer(f"Пользователь c telegram_id:{message.text} не найден!", reply_markup=general_kb.adm_kb)

@router.message(StateFilter(GeneralState.admin), F.text=="Бан")
async def set_admin_role(message:Message, state: FSMContext):
    await state.set_state(AdminStates.input_ban)
    await message.answer("Введи id пользователья, которого хочешь забанить")

@router.message(StateFilter(AdminStates.input_ban), F.text)
async def set_admin_role(message:Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(f"Введи id пользователя!", reply_markup=general_kb.adm_kb)
        return
    await state.set_state(GeneralState.admin)
    user = await AsyncUserOrm.to_ban(int(message.text))
    if user:
        await message.answer(f"Пользователь {user.telegram_username}: {user.telegram_id} забанен!", reply_markup=general_kb.adm_kb)
    else:
        await message.answer(f"Пользователь c telegram_id:{message.text} не найден!", reply_markup=general_kb.adm_kb)

@router.message(StateFilter(GeneralState.admin), F.text=="Разбан")
async def set_admin_role(message:Message, state: FSMContext):
    await state.set_state(AdminStates.input_unban)
    await message.answer("Введи id пользователья, которого хочешь разбанить")

@router.message(StateFilter(AdminStates.input_unban), F.text)
async def set_admin_role(message:Message, state: FSMContext):
    if not message.text.isnumeric():
        await message.answer(f"Введи id пользователя!", reply_markup=general_kb.adm_kb)
        return
    await state.set_state(GeneralState.admin)
    user = await AsyncUserOrm.to_admin(int(message.text))
    if user:
        await message.answer(f"Пользователь {user.telegram_username}: {user.telegram_id} разбанен!", reply_markup=general_kb.adm_kb)
    else:
        await message.answer(f"Пользователь c telegram_id:{message.text} не найден!", reply_markup=general_kb.adm_kb)

@router.message(StateFilter(GeneralState.admin), F.text=="Обращения пользователей")
async def get_report(message: Message, state: FSMContext):
    report = await AsyncReportOrm.pop_report()
    if report:
        await message.answer(f"Всего обращений осталось: {await AsyncReportOrm.get_len_reports()}\n<b>Report №{report.id}:{report.telegram_id}</b>\n{report.report}", parse_mode="HTML")
    else:
        await message.answer(f"Сейчас обращений нет!")

@router.message(StateFilter(GeneralState.admin), F.text=="Главное меню")
async def set_admin_role(message:Message, state: FSMContext):
    await state.set_state(default_state)
    await state.set_state(GeneralState.start)
    await message.answer("Добро пожаловать в главное меню! Выбери магазин:",
                         reply_markup=general_kb.main_menu_client)