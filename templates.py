from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def btn_help():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('📕 Подсказки'), KeyboardButton('🔎 Поиск фильмов'))
    kb.add(KeyboardButton('🎬 Тренды'), KeyboardButton('👻 Контакты'))
    kb.add(KeyboardButton('🔥 Подборки'))
    return kb


def btn_search_film(iframe_url: str, kinopoisk_id: int, more_btn=True):
    kb = InlineKeyboardMarkup()

    if iframe_url:
        kb.add(
            InlineKeyboardButton(
                '🍿 Смотреть онлайн',
                url=f'https://iquzy.github.io/cm?f={iframe_url}'
            )
        )
    else:
        kb.add(
            InlineKeyboardButton(
                '🔮 Кнопка для просмотра',
                callback_data=f'show_watch_btn|{kinopoisk_id}'
            )
        )

    if more_btn:
        kb.add(
            InlineKeyboardButton(
                '📙 КиноПоиск',
                url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'
            ),
            InlineKeyboardButton(
                '📙 Подробнее',
                callback_data=f'film_info|{kinopoisk_id}'
            ),
        )
    else:
        kb.add(
            InlineKeyboardButton(
                '📙 КиноПоиск',
                url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'
            )
        )
    return kb


def btn_link_to_channel():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            'Перейти в канал 👻',
            url='https://t.me/cinemoon'
        )
    )
    return kb


STATIC_TEXT_SPECIAL_HELP = """
🔎 Отправь название фильма или сериала и я покажу тебе результаты поиска

📌 Также ты можете использовать следующие команды:
⚡️ /trends - Популярные фильмы
⚡️ /search - Поиск фильмов
⚡️ /selection - Подборки 
⚡️ /contacts - Контакты
⚡️ /help - Подсказки
"""

STATIC_TEXT_SPECIAL_HELP_ADMIN = """
👷🏻‍♂️ Вы являетесь админом бота. Для вас доступны следующие команды:
⚡️ /mailing - Рассылка сообщений
⚡️ /analytics - Аналитика бота

"""

STATIC_TEXT_SPECIAL_START = """
Хеллоу, я Cinemoon 👻🍿

🔎 В моей библиотеке ты найдешь множество фильмов, сериалов, новинок киноиндустрии, а также крутые подборки и рекомендации!

⚡️Нажми кнопку "📕 Подсказки" или используй команду /help, чтобы узнать список всех моих возможностей"""

STATIC_TEXT_SPECIAL_SEARCH_FILMS = '🔎 Введите название фильма или сериала и я покажу вам результаты поиска\nИнструкция👉 t.me/cinemoon/58'

STATIC_TEXT_SPECIAL_CONTACTS = """
📝 Контакты
@iquzy - тех. поддержка, реклама 
"""

STATIC_TEXT_SPECIAL_SELECTION = '🍿 Не знаешь, что посмотреть?\nТогда переходи в наш канал @cinemoon. Здесь ты найдешь кучу крутых подборок с фильмами, мультфильмами и сериалами на свой вкус 🔥\n👉 t.me/cinemoon'

STATIC_BTN_HELP = btn_help()

STATICT_BTN_LINK_TO_CHANNEL = btn_link_to_channel()
