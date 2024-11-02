from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
callori = KeyboardButton(text="Рассчитать")
info = KeyboardButton(text="Информация")
kb.row(callori, info)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler(text=["Рассчитать"])
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост (в сантиметрах):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес (в килограммах):')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    calories = (10 * int(data["weight"])) + (6.25 * int(data["growth"])) - (5 * int(data["age"])) - 161
    await message.answer(f'Ваша дневная норма килокалорий: {calories}')
    await state.finish()



@dp.message_handler()
async def all_message(message):
    await message.answer('Введите /start, чтобы начать общение. \n'
                         'Введите "Calories", чтобы посчитать количество калорий для вас')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)
