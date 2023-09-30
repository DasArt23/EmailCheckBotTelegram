
from config import *
from aiogram import Dispatcher, Bot
from aiogram import types
from aiogram.utils import executor
from prob import getTextFromLetter
import time
import asyncio

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    time.sleep(2)
    await message.answer(getTextFromLetter())

if __name__ == "__main__":
    executor.start_polling(dp)