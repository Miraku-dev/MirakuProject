from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY, NULL
import logging
import asyncio
from os import name
import config
from aiogram.dispatcher.filters import Text
from asyncio import sleep

from keyboards import greet_kb, markuplist, product_beast, more, \
    upload_button, keyboardcontacts, keyboardlocation
from config import MY_ID, API_TOKEN
from utils import Location, available_answers_data, Admin_Panel
from pics import sucks_1, hat_1, t_shirt_1, t_shirt_2, \
    shoes_1, hoody_1, lingerie_1, pendant_1, dress_1, \
        top_1, hat_frog_cat, jeans_1, chain

from aiogram.utils.emoji import emojize
from aiogram import Bot, Dispatcher, types
from aiogram.types.message import ContentType, ContentTypes
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, ChatActions, InputMediaPhoto, user
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt


bot = Bot(token=config.API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

async def process_start_command(message: types.Message):
    await message.answer(fmt.text("Привет,", fmt.hbold(message.from_user.username), "\nЯ Григорий - бот, который облегчит работу с обработкой заказов."),
    reply_markup=greet_kb, parse_mode=types.ParseMode.HTML)

async def process_hi(message: types.Message):
    await message.answer('Пока что это всё, что я умею.', reply_markup=markuplist)

async def my_storage(message: types.Message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="Перейти", callback_data="btn5"))
    await message.answer('Вы также можете перейти в наш магазин и посмотреть список товаров там.', reply_markup=keyboard)

async def feedback(message: types.Message):
    keyboardd = types.InlineKeyboardMarkup()
    keyboardd.add(types.InlineKeyboardButton(text="Написать", callback_data="btn"))
    await message.answer('Если есть какие-либо вопросы или предложеня, напишите нам', reply_markup=keyboardd)

async def product_list(message: types.Message):
    await message.answer('Здесь вы можете посмотреть товары и их категории для примера.', reply_markup=product_beast)

async def more_beast(message: types.Message):
    await message.answer('Вот на что вы можете ещё посмотреть...', reply_markup=more)

async def help(message: types.Message):
	await message.answer('Вот, что я умею', reply_markup=markuplist)

async def process_hat_1(message: types.Message):
    caption = 'Простенькая шляпка. \n Цена: 500р.'
    caption_1 = 'Модная шляпка.\n Цена: 7500p.'
    buy_hat_1 = types.InlineKeyboardMarkup()
    buy_hat_1.add(types.InlineKeyboardButton(text="Купить", callback_data="buy_hat_1"))
    buy_hat_2 = types.InlineKeyboardMarkup()
    buy_hat_2.add(types.InlineKeyboardButton(text=f"Купить", callback_data="buy_hat_2"))
    await bot.send_photo(message.from_user.id, hat_1,
                        caption=emojize(caption), 
                         reply_to_message_id=message.message_id, reply_markup=buy_hat_1)
    await bot.send_photo(message.from_user.id, hat_frog_cat,
                        caption=emojize(caption_1),
                         reply_to_message_id=message.message_id, reply_markup=buy_hat_2)

async def process_acess(message: types.Message):
    await message.answer('Пока что здесь ничего нет, чтобы проверить функционал бота просмотрите "Головные уборы 🎩"', reply_markup=product_beast)

async def process_jeans(message: types.Message):
    await message.answer('Пока что здесь ничего нет, чтобы проверить функционал бота просмотрите "Головные уборы 🎩"', reply_markup=product_beast)

async def process_hoody(message: types.Message):
    await message.answer('Пока что здесь ничего нет, чтобы проверить функционал бота просмотрите "Головные уборы 🎩"', reply_markup=product_beast)

async def sucks(message: types.Message):
    await message.answer('Пока что здесь ничего нет, чтобы проверить функционал бота просмотрите "Головные уборы 🎩"', reply_markup=product_beast)

async def buy_hat_1(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(photo_type='Простенькая шляпка')
    await bot.send_message(call.from_user.id, text='Отправьте ваши ФИО, точный адрес и индекс, а также номер телефона.\nПожалуйста, введите эти данные ниже.',
    reply_markup=types.ReplyKeyboardRemove())
    await Location.wait_location.set()

async def buy_hat_2(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(photo_type='Модная шляпка')
    await bot.send_message(call.from_user.id, text='Отправьте ваши ФИО, точный адрес и индекс, а также номер телефона.\nПожалуйста, введите эти данные ниже.',
    reply_markup=types.ReplyKeyboardRemove())
    await Location.wait_location.set()

async def location(message: types.Message, state: FSMContext):
    await state.update_data(data_locat=message.text.title())
    await message.answer('Убедитесь в том, что данные введены верно.', reply_markup=upload_button)
    await Location.next()

async def localcation(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_answers_data:
        await message.answer("Выберите ответ, используя кнопки ниже.")
        return
    user_data = await state.get_data()
    await bot.send_message(MY_ID, fmt.text(f"Новые данные от пользователя\n@", fmt.hbold(message.from_user.username),
    f"\nПолучено следующее сообщение:"), parse_mode=types.ParseMode.HTML)
    await bot.send_message(MY_ID, f"{user_data['data_locat']}")
    await bot.send_message(MY_ID, f"Номер заказа={user_data['photo_type']}")
    await message.answer('Данные получены.')
    await message.answer('Отправьте свой контакт, чтобы мы могли с вами связаться', reply_markup=keyboardcontacts)
    await state.finish()

async def send_contact(message: types.Message):
    await bot.forward_message(MY_ID, message.chat.id, message.message_id)
    await message.answer('Теперь отправьте свою локацию, для подтверждения данных о местоположении.', reply_markup=keyboardlocation)

async def send_location(message: types.Message):
    await bot.forward_message(MY_ID, message.chat.id, message.message_id)
    await message.answer('Заказ принят в обработку. Спасибо за заказ!', reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Если хотите, можете заказать у нас что-нибудь ещё.', reply_markup=markuplist)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Вот что я умею:', reply_markup=markuplist)

async def chat_id(message):
    my_chat_id = int(message.chat.id)
    await bot.send_messag(MY_ID, my_chat_id)

def register_handlers_update(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands='start', state='*')
    dp.register_message_handler(process_hi, text='Привет! ' + emojize(':wave:'), state='*')
    dp.register_message_handler(product_list, text='Список товаров ' + emojize('🔍'), state='*')
    dp.register_message_handler(product_list, text='Назад', state='*')
    dp.register_message_handler(my_storage, text='Наш магазин ' + emojize('🪐'), state='*')
    dp.register_message_handler(feedback, text='Обратная связь ' + emojize('💬'), state='*')
    dp.register_message_handler(more_beast, text='Ещё...', state='*')
    dp.register_message_handler(help, commands=['help'], state='*')
    dp.register_message_handler(process_hat_1, text='Головные уборы 🎩', state='*')
    dp.register_message_handler(chat_id, commands=['id'], state='*')
    dp.register_message_handler(cmd_cancel, text='Отмена', state='*')
    dp.register_message_handler(buy_hat_1, text='Нет, вернуться к вводу данных', state='*')
    dp.register_message_handler(location, state=Location.wait_location)
    dp.register_message_handler(localcation, state=Location.await_location)
    dp.register_message_handler(send_contact, content_types=ContentType.CONTACT, state='*')
    dp.register_message_handler(send_location, content_types=ContentType.LOCATION, state='*')
    dp.register_message_handler(process_acess, text='Аксессуары 💍', state='*')
    dp.register_message_handler(process_hoody, text='Верхняя одежда 🧥', state='*')
    dp.register_message_handler(process_jeans, text='Брюки 👖', state='*')
    dp.register_message_handler(sucks, text='Носочки 🧦', state='*')

async def process_storage(call: types.CallbackQuery):
    await call.answer(text="По вашему желанию мы можем добавить ссылку с переходом на ваш магазин при нажатии на эту кнопку.", show_alert=True)

async def process_feedback(call: types.CallbackQuery):
    await call.answer(text='Вместо этой надписи мы можем сделать переход пользователя на любую ссылку, где он мог бы написать вам.', show_alert=True)

def register_callback_query(dp: Dispatcher):
    dp.register_callback_query_handler(process_storage, text='btn5', state='*')
    dp.register_callback_query_handler(process_feedback, text='btn', state='*')
    dp.register_callback_query_handler(buy_hat_1, text='buy_hat_1')
    dp.register_callback_query_handler(buy_hat_2, text='buy_hat_2')

async def no_command(message: types.Message):
	await message.answer('Извините, не знаю как на это ответить. Если нужна помощь - пишите /help')

def register_handlers_poop(dp: Dispatcher):
    dp.register_message_handler(no_command, content_types=ContentType.ANY, state='*')


async def main():
    logging.basicConfig(format=u'%(filename)s [ LINE:%(lineno)+3s ]#%(levelname)+8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

    bot = Bot(token=config.API_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())

    dp.middleware.setup(LoggingMiddleware())

    register_handlers_update(dp)

    register_handlers_poop(dp)

    register_callback_query(dp)

    await dp.start_polling()

async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

print("Great. Bot start success.")

if __name__ == '__main__':
    asyncio.run(main())