from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY
import logging
import asyncio
import config

from keyboards import greet_kb, markuplist, product_beast, more, \
    upload_button, keyboardcontacts, keyboardlocation
from config import MY_ID, API_TOKEN
from utils import Location, available_answers_data
from pics import sucks_1, hat_1, t_shirt_1, t_shirt_2, \
    shoes_1, hoody_1, lingerie_1, pendant_1, dress_1, \
        top_1, hat_frog_cat, jeans_1, chain

from aiogram.utils.emoji import emojize
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types.message import ContentType, ContentTypes
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode, ChatActions, InputMediaPhoto, reply_keyboard
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

async def product_list(message: types.Message):
    await message.answer('Здесь вы можете посмотреть товары и их категории для примера.', reply_markup=product_beast)

async def more_beast(message: types.Message):
    await message.answer('Вот на что вы можете ещё посмотреть...', reply_markup=more)

async def help(message: types.Message):
	await message.answer('Вот, что я умею', reply_markup=markuplist)

async def process_hat_1(message: types.Message):
    caption = 'Простенькая шляпка. \n Цена: 500р.'
    caption_1 = 'Модная шляпка.\n Цена: 7500p.'
    await bot.send_photo(message.from_user.id, hat_1,
                        caption=emojize(caption),
                         reply_to_message_id=message.message_id)
    await bot.send_photo(message.from_user.id, hat_frog_cat,
                        caption=emojize(caption_1),
                         reply_to_message_id=message.message_id)

async def location_date(message: types.Message):
    await message.answer('Отправьте ваши ФИО, точный адрес и индекс, а также номер телефона.\nПожалуйста, введите эти данные ниже.',
    reply_markup=types.ReplyKeyboardRemove())
    await Location.wait_location.set()

async def location(message: types.Message, state: FSMContext):
    await state.update_data(data_locat=message.text.lower())
    await message.answer('Убедитесь в том, что данные введены верно.', reply_markup=upload_button)
    await Location.next()

async def localcation(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_answers_data:
        await message.answer("Выберите ответ, используя кнопки ниже.")
        return
    user_data = await state.get_data()
    await bot.send_message(MY_ID, fmt.text(f"Новые данные от пользователя\n@", fmt.hbold(message.from_user.username),
    f"\nПолучено следующее сообщение:\n{user_data['data_locat']}"), parse_mode=types.ParseMode.HTML)
    await message.answer('Данные получены.')
    await message.answer('Отправьте свой контакт, чтобы мы могли с вами связаться', reply_markup=keyboardcontacts)
    await state.finish()

async def send_contact(message: types.Message):
    await bot.forward_message(MY_ID, message.chat.id, message.message_id)
    await message.answer('Теперь отправьте свою локацию, для подтверждения данных о местоположении', reply_markup=keyboardlocation)

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
    dp.register_message_handler(more_beast, text='Ещё...', state='*')
    dp.register_message_handler(help, commands=['help'], state='*')
    dp.register_message_handler(process_hat_1, text='Головные уборы 🎩', state='*')
    dp.register_message_handler(chat_id, commands=['id'], state='*')
    dp.register_message_handler(cmd_cancel, text='Отмена', state='*')
    dp.register_message_handler(location_date, text='Купить', state='*')
    dp.register_message_handler(location_date, text='Нет, вернуться к вводу данных', state='*')
    dp.register_message_handler(location, state=Location.wait_location)
    dp.register_message_handler(localcation, state=Location.await_location)
    dp.register_message_handler(send_contact, content_types=ContentType.CONTACT, state='*')
    dp.register_message_handler(send_location, content_types=ContentType.LOCATION, state='*')

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

    await dp.start_polling()

print("Great. Bot start success.")

if __name__ == '__main__':
    asyncio.run(main())