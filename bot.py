from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

battlesKeys = {}
lastId = 0

class TestStates(Helper):
    mode = HelperMode.snake_case

    TEST_STATE_0 = ListItem()
    TEST_STATE_1 = ListItem()
    TEST_STATE_2 = ListItem()
    TEST_STATE_3 = ListItem()
    TEST_STATE_4 = ListItem()
    TEST_STATE_5 = ListItem()

from config import TOKEN

MESSAGES = {'start': 'Привет, как дела', 'help':'ща как помогу!', 'state_change': 'ЕСТЬ', 'state_reset': 'ЕСТЬ ОБРАТНО!'}

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply(MESSAGES['start'])


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply(MESSAGES['help'])

@dp.message_handler(commands=['battle'])
async def process_help_command(message: types.Message):
    global lastId, battlesKeys
    id = lastId + 1
    lastId = id
    battlesKeys[id] = [message.from_user.id]
    await message.reply('Ваш id боя: ' + str(id))
    state = dp.current_state(user=message.from_user.id)
    await state.set_state(TestStates.all()[2])


@dp.message_handler(state='*', commands=['setstate'])
async def process_setstate_command(message: types.Message):
    argument = message.get_args()
    state = dp.current_state(user=message.from_user.id)
    if not argument:
        await state.reset_state()
        return await message.reply(MESSAGES['state_reset'])

    if (not argument.isdigit()) or (not int(argument) < len(TestStates.all())):
        return await message.reply(MESSAGES['invalid_key'].format(key=argument))

    await state.set_state(TestStates.all()[int(argument)])
    await message.reply(MESSAGES['state_change'], reply=False)

@dp.message_handler(state=TestStates.TEST_STATE_1)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Тут будет изменение статов самолета', reply=False)


@dp.message_handler(state=TestStates.TEST_STATE_2)
async def first_test_state_case_met(message: types.Message):
    await message.reply('Тут будет бой', reply=False)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()

if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)