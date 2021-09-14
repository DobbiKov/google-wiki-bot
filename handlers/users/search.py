from typing import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types.message import Message
from states.search_state import Search
from keyboards.inline.start_inline import start_inline

from utils.consts import CALLBACK_DATA_SEARCH_GOOGLE, CALLBACK_DATA_SEARCH_WIKIPEDIA, CALLBACK_DATA_TRANSLATE_EN, CALLBACK_DATA_TRANSLATE_RU

from loader import dp, bot

@dp.message_handler(content_types=types.ContentTypes.TEXT, state=None)
async def start_search(message: types.Message, state: FSMContext):
    # await state.update_data(search=message.text.lower())
    # # Для последовательных шагов можно не указывать название состояния, обходясь next()
    # await Search.next()
    await message.reply("Где ищем?", reply_markup=start_inline())

@dp.callback_query_handler()
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    # _state = await state.get_data()
    # print(_state['search'])
    print(call.data)
    if not call.data.startswith("dobbi_search"):
        return print("BAD!")
    
    if call.data == CALLBACK_DATA_SEARCH_GOOGLE:
        print("!")
        await call.message.reply("GOOGLE!")
    if call.data == CALLBACK_DATA_SEARCH_WIKIPEDIA:
        await call.message.reply("WIKI!")
    if call.data == CALLBACK_DATA_TRANSLATE_RU:
        await call.message.reply("RU!")
    if call.data == CALLBACK_DATA_TRANSLATE_EN:
        await call.message.reply("EN!")

    await bot.delete_message(call.message.chat.id, call.message.message_id)