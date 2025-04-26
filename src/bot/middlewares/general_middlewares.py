from datetime import datetime, timedelta
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject, CallbackQuery
from collections import defaultdict
from typing import Dict, Any, Callable, Awaitable

from src.database.orm import AsyncUserOrm

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self, cooldown_seconds: int = 1, max_calls: int = 3):
        self.cooldown = cooldown_seconds
        self.max_calls = max_calls
        self.user_calls = defaultdict(list)

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, Message):
            # Если это не сообщение, пропускаем
            return await handler(event, data)

        user_id = event.from_user.id
        now = datetime.now()

        # Удаляем старые вызовы (> cooldown)
        self.user_calls[user_id] = [
            t for t in self.user_calls[user_id]
            if now - t < timedelta(seconds=self.cooldown)
        ]

        if len(self.user_calls[user_id]) >= self.max_calls:
            await event.answer("⚠️ Слишком много запросов! Подождите немного.")
            return 

        self.user_calls[user_id].append(now)
        return await handler(event, data)

class BanCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        if not isinstance(event, (Message, CallbackQuery)):
            # Если это не сообщение или запрос на callback, пропускаем
            return await handler(event, data)


        user_id = event.from_user.id
        user = await AsyncUserOrm.get_user(user_id)

        if user and user.is_banned:
            if isinstance(event, CallbackQuery):
                await event.answer(
                    "🚫 Вы заблокированы!\nЗа разбаном обратитесь к <b>@rezdom</b>",
                    show_alert=True,
                    parse_mode="HTML"
                )
            elif isinstance(event, Message):
                await event.answer(
                    "🚫 Вы заблокированы!\nЗа разбаном обратитесь к <b>@rezdom</b>",
                    parse_mode="HTML"
                )
            return

        
        return await handler(event, data)
