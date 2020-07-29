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
    '^(.+)$': bfunc.search_films,
})

hl.add('/mailing', {
    '^(.*|.+)$': bfunc.mailing_text
})

hl.add('/mailing_verify', {
    '^(Старт)$': bfunc.mailing_start,
    '^(Отмена)$': bfunc.mailing_cancel,
})

hl.add('special', {
    '^(/start)$': bfunc.special_start,
    '^(📕 Подсказки|/help)$': bfunc.special_help,
    '^(/popular)$': bfunc.popular_films,
    '^(/mailing)$': bfunc.special_mailing
})

hl.add_query('^(show_watch_btn|.+)$', bfunc.query_show_watch_btn)


@dp.message_handler(content_types=types.ContentType.ANY)
async def handler(m: types.Message):
    logging.info(f'[Message] From: {m.from_user.full_name}(@{m.from_user.username}) | Text: {m.text}')
    await hl.handle_message(m)


@dp.callback_query_handler()
async def handler(c: types.CallbackQuery):
    await hl.handle_query(c)

def start():
    try:
        executor.start_polling(dp, skip_updates=True)
    except:
        time.sleep(15)
        start()


if __name__ == '__main__':
    start()
