from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

available_answers_data = ['да, всё верно.', 'нет, вернуться к вводу данных']

class Location(StatesGroup):
    wait_location = State()
    await_location = State()