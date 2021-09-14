from logging import log
from typing import Text
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import user
from aiogram.types.message import Message
from environs import LogLevelField
from states.search_state import Search
from keyboards.inline.start_inline import start_inline
from utils.search.search import search as utilsearch
from utils.wikipedia import wikipediaSearch

from utils.consts import CALLBACK_DATA_SEARCH_GOOGLE, CALLBACK_DATA_SEARCH_WIKIPEDIA, CALLBACK_DATA_TRANSLATE_EN, CALLBACK_DATA_TRANSLATE_RU, CLOSE_INLINE_MESSAGE

from loader import dp, bot

from data.config import ADMINS

@dp.callback_query_handler(lambda c: c.data == CALLBACK_DATA_SEARCH_WIKIPEDIA)
async def choose_search(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        text = "null"
        text = data.get("search")

        markup3 = types.InlineKeyboardMarkup()
        if(text != "null"):
            [text, markup3] = await bot_choose_search(call, state, text)
        else:
            text = "Error!"
        # print(text)

        
        await bot.send_message(call.from_user.id, text, reply_markup=markup3)
    except Exception as ex:
        print(ex)
        await bot.send_message(call.from_user.id, f"Технические неполадки, приносим свои извинения.")
        for admin in ADMINS:
            
            await bot.send_message(admin, f"У пользователя {call.from_user.full_name} произошла ошибка при поиске!")

    await bot.delete_message(call.message.chat.id, call.message.message_id)

async def bot_choose_search(call: types.CallbackQuery, state: FSMContext, text: str):
    markup3 = types.InlineKeyboardMarkup()
    arr = wikipediaSearch.search("ru", text)
    if arr[0] == []:
        text = "Вариантов ответа по вашему запросу не найдено!"
    else:
        text = "Варианты ответа по вашему запросу:"
        wikipediaSearches = arr[0]
        steps = 0
        for i in arr[0]:
            if i == "":
                continue
            try:
                button = types.InlineKeyboardButton(i, callback_data="d_wiki_s_{0}".format(arr[0].index(i)))
            except:
                continue
            steps += 1
            markup3.add(button)

        state = dp.current_state(chat=call.from_user.id, user=call.from_user.id)
        await state.update_data(wikipediaSearches=wikipediaSearches)
        _button = types.InlineKeyboardButton("Закрыть", callback_data=CLOSE_INLINE_MESSAGE)
        markup3.add(_button)
    return [text, markup3]

@dp.callback_query_handler(lambda c: c.data.startswith("d_wiki_s_"))
async def choose_article(call: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()

        text = "null"
        text = data.get("wikipediaSearches")

        markup3 = types.InlineKeyboardMarkup()
        if(text != "null"):
            [text, markup3] = await botWikipediaArticle(call, state, text)
        else:
            text = "Error!"
        # print(text)

        
        await bot.send_message(call.from_user.id, text, reply_markup=markup3)
        await state.finish()
    except Exception as ex:
        print(ex)
        await bot.send_message(call.from_user.id, f"Технические неполадки, приносим свои извинения.")
        for admin in ADMINS:
            
            await bot.send_message(admin, f"У пользователя {call.from_user.full_name} произошла ошибка при поиске!")

    await bot.delete_message(call.message.chat.id, call.message.message_id)

async def botWikipediaArticle(call: types.CallbackQuery, state: FSMContext, wikiSearch):

    text = call.data.replace("d_wiki_s_", "")
    ourSearch = wikiSearch[int(text)]
    userId = call.from_user.id
    _button = types.InlineKeyboardButton("Закрыть", callback_data=CLOSE_INLINE_MESSAGE)
    markup3 = types.InlineKeyboardMarkup()

    if ourSearch == None or ourSearch == "":
        markup3.add(_button)
        return ["Возникла техническая ошибка. Приносим свои извинения.", markup3]

    article = "{0}\n\n".format(ourSearch)
    tempArticle = wikipediaSearch.article("ru", ourSearch)
    if tempArticle == None or tempArticle == "":
        markup3.add(_button)
        return ["Возникла техническая ошибка. Приносим свои извинения.", markup3]
    article += tempArticle

    
    link = wikipediaSearch.link("ru", ourSearch)
    if link != "" and link != None:
        button = types.InlineKeyboardButton("Ссылка", url=link)
        markup3.add(button)
    markup3.add(_button)
    return [article, markup3]