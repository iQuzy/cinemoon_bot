import logging
import time
from aiogram import Bot, Dispatcher, executor, types

from lib.handler import hl
from config import BOT_TOKEN
import bfunc


logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

hl.add('/', {
    'Поиск фильмов': bfunc.home_find,
    '.*': bfunc.home_default,
})

hl.add('/films_search', {
    '.*': bfunc.films_search
})

hl.add('special', {
    'Назад': bfunc.specil_home
})


@dp.message_handler()
async def handler(m: types.Message):
    logging.info(f'[Message] From: {m.from_user.full_name} | Text: {m.text}')
    await hl.handle_message(m)


def start():
    try:
        executor.start_polling(dp, skip_updates=True)
    except:
        time.sleep(15)
        start()


if __name__ == '__main__':
    start()
