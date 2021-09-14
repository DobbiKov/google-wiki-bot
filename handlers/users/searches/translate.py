from keyboards.inline.close_keyboard import close_keyboard
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.inline.start_inline import start_inline
from utils.search.search import search as utilsearch
from mtranslate import translate

from utils.consts import CALLBACK_DATA_TRANSLATE_EN, CALLBACK_DATA_TRANSLATE_RU

from loader import dp, bot

from data.config import ADMINS

@dp.callback_query_handler(lambda c: c.data == CALLBACK_DATA_TRANSLATE_RU)
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    await botTranslate(call, state, "ru")

    await bot.delete_message(call.message.chat.id, call.message.message_id)

@dp.callback_query_handler(lambda c: c.data == CALLBACK_DATA_TRANSLATE_EN)
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    await botTranslate(call, state, "en")

    await bot.delete_message(call.message.chat.id, call.message.message_id)

async def botTranslate(call: types.CallbackQuery, state: FSMContext, lang: str):
    try:
        data = await state.get_data()
        search = data.get("search")

        text = translate(search, lang, "auto")
        await bot.send_message(call.from_user.id, text or "Error", reply_markup=close_keyboard())
        await state.finish()
    except Exception as ex:
        print(ex)
        await bot.send_message(call.from_user.id, f"Технические неполадки, приносим свои извинения.")
        for admin in ADMINS:
            
            await bot.send_message(admin, f"У пользователя {call.from_user.full_name} произошла ошибка при переводе!")