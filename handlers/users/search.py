from logging import log
from typing import Text
from utils.consts import CLOSE_INLINE_MESSAGE

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import user
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types.message import Message
from environs import LogLevelField
from keyboards.inline.start_inline import start_inline
from loader import bot, dp
from states.search_state import Search
from utils.search.search import search as utilsearch


@dp.message_handler(content_types=types.ContentTypes.TEXT, state=None)
async def start_search(message: types.Message, state: FSMContext):
    
    state = dp.current_state(chat=message.chat.id, user=message.from_user.id)
    await state.update_data(search=message.text.lower())

    await message.reply("Где ищем?", reply_markup=start_inline())