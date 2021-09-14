from aiogram.types import user, InlineKeyboardButton, InlineKeyboardMarkup
from utils.consts import CLOSE_INLINE_MESSAGE

def close_keyboard():
    keyboard = InlineKeyboardMarkup()

    button = InlineKeyboardButton("Закрыть", callback_data=CLOSE_INLINE_MESSAGE)

    keyboard.add(button)
    return keyboard