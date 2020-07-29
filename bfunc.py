from aiogram.types import Message, CallbackQuery
from lib.handler import hl
from lib.hdvbDriver import hdvb
import botkb
import config


class MailingData:
    text: str
    photo_id: str
    caption: str

    def __init__(self):
        self.text = ''
        self.photo_id = ''
        self.caption = ''


mailing_data = MailingData()


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
            await m.answer_photo(film.poster, caption=caption, reply_markup=botkb.search_film(film.iframe_url, film.kinopoisk_id))
    else:
        await m.answer('Простите, я ничего не нашел', reply_markup=botkb.static_help)


async def popular_films(m: Message):
    films = await hdvb.get_popular_films()
    if films:
        for film in films:
            caption = "🎬{title} ({year}{quality})".format(
                title=film.title,
                year=str(film.year) + '/' if film.year else '',
                quality=film.quality
            )
            await m.answer_photo(film.poster, caption=caption, reply_markup=botkb.search_film(film.iframe_url, film.kinopoisk_id))
    else:
        await m.answer('Рейтинг пуст')


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
            await m.bot.send_message(user_id[0], mailing_data.text)

        elif mailing_data.photo_id:
            await m.bot.send_photo(user_id[0], photo=mailing_data.photo_id, caption=mailing_data.caption)
        k += 1

    await m.answer(f'📩 Рассылка закончена. Кол-во отправленных сообщений: {k}')
    mailing_data = MailingData()


async def mailing_cancel(m: Message):
    global mailing_data

    mailing_data = MailingData()
    hl.set_user_path('/', m.from_user.id)
    await m.answer('Рассылка отменена')


async def special_help(m: Message):
    text = """
🔎 Для поиска отправьте название фильма или сериала

📌 Также вы можете использовать следующие команды:
/popular - Популярные фильмы
/help - Подсказки

📝 Контакты:
@iquzy - тех. поддержка, реклама 
"""

    text_for_admin = """
👷🏻‍♂️ Вы являетесь админом бота. Для вас есть следующие команды:
/mailing - Рассылка сообщений пользователям    
"""
    await m.answer(text)

    if m.from_user.id == config.ADMIN_ID:
        await m.answer(text_for_admin)


async def special_start(m: Message):
    text = """
Хеллоу, я Cinemoon 👻🤖

🔎 В моей библиотеке ты найдешь множество фильмов, сериалов и новинок киноиндустрии!

📌 Используй команду /help или нажми на кнопку "📕 Подсказки", чтобы узнать, как правильно пользоваться мной
"""
    await m.answer(text, reply_markup=botkb.static_help)


async def special_mailing(m: Message):
    if m.from_user.id == config.ADMIN_ID:
        await m.answer('📝 Введите текст сообщения')
        hl.set_user_path('/mailing', m.from_user.id)


async def query_show_watch_btn(c: CallbackQuery):
    kp_id: int = int(c.data.split('|')[1])
    film = await hdvb.find_by_kp_id(kp_id)

    if film.kinopoisk_id:
        await c.bot.edit_message_reply_markup(c.from_user.id, c.message.message_id,
                                              reply_markup=botkb.search_film(film.iframe_url, film.kinopoisk_id, True))
        await hdvb.up_film_rating(film)
    else:
        c.answer('Ошибка')
