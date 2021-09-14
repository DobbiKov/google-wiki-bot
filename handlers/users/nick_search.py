from utils.consts import CLOSE_INLINE_MESSAGE
from aiogram import types
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.start_inline import start_inline
from loader import bot, dp
from states.search_state import Search
from utils.search.search import search as utilsearch



@dp.message_handler(lambda message: message.text.startswith("@"), content_types=types.ContentTypes.TEXT, state=None, )
async def start_search(message: types.Message):
    
    nick = message.text.replace("@", "")
    keyboard = InlineKeyboardMarkup()
    _button = types.InlineKeyboardButton("Закрыть", callback_data=CLOSE_INLINE_MESSAGE)

    inst = types.InlineKeyboardButton("Instagram", url=f"https://instagram.com/{nick}")
    vk = types.InlineKeyboardButton("Вконтакте", url=f"https://vk.com/{nick}")
    facebook = types.InlineKeyboardButton("Facebook", url=f"https://facebook.com/{nick}")
    twitter = types.InlineKeyboardButton("Twitter", url=f"https://twitter.com/{nick}")
    
    keyboard.add(inst)
    keyboard.add(vk)
    keyboard.add(facebook)
    keyboard.add(twitter)
    keyboard.add(_button)
    await message.reply("Поиск ника по соц.сетям:", reply_markup=keyboard)