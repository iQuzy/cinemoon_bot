from aiogram.types import Message, CallbackQuery
from app import hl, hdvb
import templates
import config
import time


class MailingData:
    text: str
    photo_id: str
    caption: str

    def __init__(self):
        self.text = ''
        self.photo_id = ''
        self.caption = ''


mailing_data = MailingData()
date_step = 86_400  # 24 часа (в секундах)
next_date = int(time.time()) + date_step
views_of_day = 0


async def search_films(m: Message):
    await m.answer(f'🔎 Идёт поиск фильма "{m.text}"')

    films = await hdvb.find_by_title(m.text, limit=25)

    if films:
        for film in films:
            caption = '🎬{title} ({year}{quality})'.format(
                title=film.title,
                year=str(film.year) + '/' if film.year else '',
                quality=film.quality
            )
            await m.answer_photo(
                photo=film.poster,
                caption=caption,
                reply_markup=templates.btn_search_film('', film.kinopoisk_id)
            )
    else:
        await m.answer('Простите, я ничего не нашел', reply_markup=templates.STATIC_BTN_HELP)


async def mailing_text(m: Message):
    global mailing_data

    if m.text:
        mailing_data.text = m.text
    elif m.photo:
        mailing_data.photo_id = m.photo[0].file_id
        mailing_data.caption = m.caption
    else:
        await m.answer('Некорректное сообщение')
        return
    hl.set_user_path('/mailing_verify', m.from_user.id)

    await m.answer('Напишите "Старт" - чтобы начать рассылку, или "Отмена"')


async def mailing_start(m: Message):
    global mailing_data

    all_user_ids = hl.get_all_ids()

    k = 0

    await m.answer('📤 Бот начал рассылку')
    hl.set_user_path('/', m.from_user.id)

    for user_id in all_user_ids:
        if mailing_data.text:
            await m.bot.send_message(user_id, mailing_data.text)

        elif mailing_data.photo_id:
            await m.bot.send_photo(user_id, photo=mailing_data.photo_id, caption=mailing_data.caption)
        k += 1

    await m.answer(f'📩 Рассылка закончена. Кол-во отправленных сообщений: {k}')
    mailing_data = MailingData()


async def mailing_cancel(m: Message):
    global mailing_data

    mailing_data = MailingData()
    hl.set_user_path('/', m.from_user.id)
    await m.answer('Рассылка отменена')


async def special_search_films(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_SEARCH_FILMS)


async def special_popular_films(m: Message):
    films = await hdvb.get_popular_films()
    if films:
        n = 1
        for film in films:
            caption = "{n}. 🎬{title} ({year}{quality})".format(
                n=n,
                title=film.title,
                year=str(film.year) + '/' if film.year else '',
                quality=film.quality
            )
            await m.answer_photo(
                photo=film.poster,
                caption=caption,
                reply_markup=templates.btn_search_film('', film.kinopoisk_id)
            )
            n += 1
    else:
        await m.answer('Рейтинг пуст')


async def special_contacts(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_CONTACTS)


async def special_help(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_HELP, reply_markup=templates.STATIC_BTN_HELP)

    if m.from_user.id == config.ADMIN_ID:
        await m.answer(templates.STATIC_TEXT_SPECIAL_HELP_ADMIN)


async def special_start(m: Message):
    await m.answer(templates.STATIC_TEXT_SPECIAL_START, reply_markup=templates.STATIC_BTN_HELP)


async def special_mailing(m: Message):
    if m.from_user.id == config.ADMIN_ID:
        await m.answer('📝 Введите текст сообщения')
        hl.set_user_path('/mailing', m.from_user.id)


async def special_statistics(m: Message):
    global next_date, date_step, views_of_day

    if time.time() > next_date:
        next_date = int(time.time()) + date_step
        views_of_day = 0

    t = '📊 Статистика бота\n\n' \
        + f'👨🏻‍💻 Кол-во юзеров: {len(hl.get_all_ids())}\n'\
        + f'👀 Просмотров за сутки: {views_of_day}'

    await m.answer(t)


async def query_show_watch_btn(c: CallbackQuery):
    global views_of_day, next_date, date_step

    kp_id: int = int(c.data.split('|')[1])
    film = await hdvb.find_by_kp_id(kp_id)

    if time.time() > next_date:
        next_date = int(time.time()) + date_step
        views_of_day = 0

    views_of_day += 1

    if film.kinopoisk_id:
        await c.bot.edit_message_reply_markup(
            chat_id=c.from_user.id,
            message_id=c.message.message_id,
            reply_markup=templates.btn_search_film(
                film.iframe_url,
                film.kinopoisk_id,
                more_btn=False
            )
        )
        await hdvb.up_film_rating(film)
    else:
        c.answer('Ошибка')


async def query_film_info(c: CallbackQuery):
    kp_id = int(c.data.split('|')[1])
    film_info = await hdvb.get_film_info(kp_id)

    new_caption = c.message.caption \
        + f'\n\n⏳ Время: {film_info.length} (часы) \n\n🎥 Жанры: {", ".join(film_info.genres)} \n\n📙 Описание: {film_info.description}'

    await c.answer('Описание получено 👌')

    await c.bot.edit_message_caption(
        c.from_user.id,
        c.message.message_id,
        caption=new_caption,
        reply_markup=templates.btn_search_film('', kp_id, more_btn=False)
    )
