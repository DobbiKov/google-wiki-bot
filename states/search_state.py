from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class Search(StatesGroup):
    search = State("")
    wikipediaSearch = State("")