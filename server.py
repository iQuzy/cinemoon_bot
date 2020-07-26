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
    '^(Поиск фильмов|/search_films)$': bfunc.home_find,
    '.*': bfunc.home_default,
})

hl.add('/search_films', {
    '.*': bfunc.search_films
})

hl.add('special', {
    '^(💃 Назад|/back)$': bfunc.specil_home
})

# hl.add_query('^(film_info_.*)$', bfunc.query_film_info)


@dp.message_handler()
async def handler(m: types.Message):
    logging.info(f'[Message] From: {m.from_user.full_name} | Text: {m.text}')
    await hl.handle_message(m)

@dp.callback_query_handler()
async def handler(c: types.CallbackQuery):
    await hl.handle_query(c)
    # await bot.edit_message_caption(c.from_user.id, c.message.message_id, caption="edit")

def start():
    try:
        executor.start_polling(dp, skip_updates=True)
    except:
        time.sleep(15)
        start()


if __name__ == '__main__':
    start()
