import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher.handler import CancelHandler

from aiogram.dispatcher.storage import FSMContext

from create_bot import bot

'''
Middlewares - файл для настройки мидлвари(прослойки между апи телеграмма и сервером),
которая помогает нам обрабатывать updates до handler'ов.

В данном случае я реализовал антифлуд систему
'''

class ThrottledMiddlware(BaseMiddleware): #Создаю класс для реализации кастомных мидлвари
    def __init__(self, limit: int=3):
        BaseMiddleware.__init__(self)
        self.rate_limit = limit
    
    async def on_process_message(self, msg:types.Message, data: dict): #кастомный этап по обработке мидлвари
        dp = Dispatcher.get_current()
        state = Dispatcher.current_state(dp)
        try:
            await dp.throttle(key='antiflood_message', rate=self.rate_limit)
        except Throttled as _t:
            await self.throttle_msg(msg,_t,state)

            raise CancelHandler()
    
    async def throttle_msg(self, msg:types.Message, throttled: Throttled, state: FSMContext): #алгоритм, чтобы накладывать таймаут на флуд
        delta = throttled.rate - throttled.delta
        if throttled.exceeded_count <= 2:
            msg = await msg.answer(text="Перестань флудить, подожди некоторое время!")
            async with state.proxy() as data:
                if 'last_msg' in data:
                    await bot.delete_message(chat_id=msg.chat.id, message_id=data['last_msg'])
                data['last_msg'] = msg.message_id
            await asyncio.sleep(delta)