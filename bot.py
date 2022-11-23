from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЯ бот для боев на самолетиках! \nЧтобы начать свой бой напиши /battle\nЧтобы подключиться к бою нажмите /connect\nЧтобы изменть конфигурацию своего самолета нажмите /config")

@dp.message_handler(commands=['battle'])
async def process_help_command(message: types.Message):
    await message.reply("Тут будет старт боя")

@dp.message_handler(commands=['connect'])
async def process_help_command(message: types.Message):
    await message.reply("Тут будет подключение к бою")

@dp.message_handler(commands=['config'])
async def process_help_command(message: types.Message):
    await message.reply("Тут будут статы самолетика")


if __name__ == '__main__':
    executor.start_polling(dp)