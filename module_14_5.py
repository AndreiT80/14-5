# Домашнее задание по теме "Написание примитивной ORM"



from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from crud_functions import *
import asyncio



api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text="Расчитать")
button2 = KeyboardButton(text="Информация")
button1 = KeyboardButton(text="Купить")
button9 = KeyboardButton(text="Регистрация")
kb.row(button, button2)
kb.add(button9)
kb.insert(button1)

kb1 = InlineKeyboardMarkup()
button3 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button4 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb1.add(button3)
kb1.insert(button4)

kb2 = InlineKeyboardMarkup()
button5 = InlineKeyboardButton(text='Product1', callback_data='product_buying')
button6 = InlineKeyboardButton(text='Product2', callback_data='product_buying')
button7 = InlineKeyboardButton(text='Product3', callback_data='product_buying')
button8 = InlineKeyboardButton(text='Product4', callback_data='product_buying')
kb2.row(button5, button6, button7, button8)


@dp.message_handler(commands=['start'])
async def start_message(message):
     await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = State()


@dp.message_handler(text='Регистрация')
async def sign_up(message):
    await message.answer('Введите имя пользователя (только латинские буквы)')
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    is_inc = is_included(message.text)
    if is_inc is True:
        await message.answer('Данное имя уже занято, введите другое')
    else:
        await state.update_data(username=message.text)
        data = await state.get_data()
        await message.answer('Введите свой email')
        await RegistrationState.email.set()

@dp.message_handler(state=RegistrationState.email)
async def set_age(message, state):
    await state.update_data(email=message.text)
    data = await state.get_data()
    await message.answer('Введите свой возраст')
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def end_of_reg(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    add_user(data['username'], data['email'], data['age'])
    await state.finish()
    await message.answer('Поздравляем с вступлением в наш клуб, на вашем балансе'
                         ' приветсвенные 1000 баллов',reply_markup=kb)


sid = get_all_products()

@dp.message_handler(text = 'Купить')
async def  get_buying_list(message):
    with open("files/1.png", "rb") as img:
        await message.answer(f"Название: {sid[0][1]} | Описание: {sid[0][2]} | Цена: {sid[0][3]} руб.")
        await message.answer_photo(img)
    with open("files/2.png", "rb") as img:
        await message.answer(f"Название: {sid[1][1]} | Описание: {sid[1][2]} | Цена: {sid[1][3]} руб.")
        await message.answer_photo(img)
    with open("files/3.png", "rb") as img:
        await message.answer(f"Название: {sid[2][1]} | Описание: {sid[2][2]} | Цена: {sid[2][3]} руб.")
        await message.answer_photo(img)
    with open("files/4.png", "rb") as img:
        await message.answer(f"Название: {sid[3][1]} | Описание: {sid[3][2]} | Цена: {sid[3][3]} руб.")
        await message.answer_photo(img)
    await message.answer(text='Выберите продукт для покупки:', reply_markup=kb2)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()


@dp.message_handler(text=["Расчитать"])
async def set_age(message):
    await message.answer("Выберите опцию:", reply_markup=kb1)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('10 x вес (кг) + 6,25 х рост (см) - 5 х возраст (г) - 5')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def get_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state=UserState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer("Ввeдите свой рост:")
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_growth(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer("Введите свой вес:")
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = 10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) + 5
    await message.answer(f'Ваши калории {calories}')
    await state.finish()

@dp.message_handler(text=["Информация"])
async def inform(message):
    await message.answer("Информация о Боте")


@dp.message_handler()
async def all_message(message):
        await message.answer('Введите команду /start, чтобы начать общение.')




if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

