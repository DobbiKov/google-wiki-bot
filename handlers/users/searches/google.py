from keyboards.inline.close_keyboard import close_keyboard
from logging import log
from typing import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import user, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message
from environs import LogLevelField
from states.search_state import Search
from keyboards.inline.start_inline import start_inline
from utils.search.search import search as utilsearch

from utils.consts import CALLBACK_DATA_SEARCH_GOOGLE

from loader import dp, bot

from data.config import ADMINS

@dp.callback_query_handler(lambda c: c.data == CALLBACK_DATA_SEARCH_GOOGLE)
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        search = data.get("search")

        searches = utilsearch(search)
        await bot.send_message(call.from_user.id, searches or "Error", reply_markup=close_keyboard())
        await state.finish()
    except Exception as ex:
        print(ex)
        await bot.send_message(call.from_user.id, f"Технические неполадки, приносим свои извинения.")
        for admin in ADMINS:
            
            await bot.send_message(admin, f"У пользователя {call.from_user.full_name} произошла ошибка при поиске!")

    await bot.delete_message(call.message.chat.id, call.message.message_id)