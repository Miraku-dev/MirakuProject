import aiogram

from aiogram.utils.emoji import emojize

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton, contact

button_hi = KeyboardButton('Привет! 👋')

button_upload1 = KeyboardButton('Да, всё верно.')
button_upload2 = KeyboardButton('Нет, вернуться к вводу данных')
button_upload3 = KeyboardButton('Отмена')

button_list_1 = KeyboardButton('Список товаров ' + emojize('🔍'))
button_list_3 = KeyboardButton('Наш магазин ' + emojize('🪐'))
button_list_4 = KeyboardButton('Обратная связь ' + emojize('💬'))

product_list_1 = KeyboardButton('Головные уборы ' + emojize('🎩'))
product_list_2 = KeyboardButton('Аксессуары ' + emojize('💍'))
product_list_3 = KeyboardButton('Футболки ' + emojize('👕'))
product_list_4 = KeyboardButton('Брюки ' + emojize('👖'))
product_list_5 = KeyboardButton('Верхняя одежда ' + emojize('🧥'))
product_list_6 = KeyboardButton('Ещё...')
product_list_7 = KeyboardButton('Носочки ' + emojize('🧦'))
product_list_8 = KeyboardButton('Нижнее бельё ' + emojize('🩲'))

keyboardcontacts = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton('Отправить свой контакт ☎️', request_contact=True)
)
keyboardlocation = ReplyKeyboardMarkup(resize_keyboard=True).add(
        KeyboardButton('Отправить своё местоположение 🗺️', request_location=True)
)

upload_button = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_upload1).add(button_upload2).add(button_upload3)

greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(button_hi)

inline_btn_1 = InlineKeyboardButton('Первая кнопка!', callback_data='button1')
inline_kb1 = InlineKeyboardMarkup().add(inline_btn_1)

markuplist = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    button_list_1).add(button_list_3).add(button_list_4)

product_beast = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    product_list_1).add(product_list_2).add(product_list_5).add(product_list_3).add(product_list_6)

more = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(
    product_list_7).add(product_list_8)