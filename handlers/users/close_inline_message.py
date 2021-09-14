from logging import log
from typing import Text
from aiogram import types
from aiogram.dispatcher import FSMContext

from utils.consts import CLOSE_INLINE_MESSAGE

from loader import dp, bot

@dp.callback_query_handler(lambda c: c.data == CLOSE_INLINE_MESSAGE)
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.message.chat.id, call.message.message_id)
    await state.finish()