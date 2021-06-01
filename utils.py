from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

available_answers_data = ['да, всё верно.', 'нет, вернуться к вводу данных']

class Location(StatesGroup):
    photo_type = State()
    wait_location = State()
    await_location = State()

class Admin_Panel(StatesGroup):
    Name = State()
    Photo = State()
    Caption = State()
    Confirm = State()