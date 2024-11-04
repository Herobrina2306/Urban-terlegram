from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb_bottom = ReplyKeyboardMarkup(resize_keyboard=True)
callori = KeyboardButton(text="Рассчитать")
info = KeyboardButton(text="Информация")
kb_bottom.row(callori, info)

kb_top = InlineKeyboardMarkup()
rass = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='callories')
form = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_top.add(rass)
kb_top.add(form)

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands=["start"])
async def start_message(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb_bottom)


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_top)
    await UserState.age.set()


@dp.callback_query_handler(text='formulas')
async def cillback_query_handler(call):
    await call.message.answer('10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text="callories")
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await call.answer()
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
    await message.answer('Введите /start, чтобы начать общение.')

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates= True)
