from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def btn_help():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('📕 Подсказки'), KeyboardButton('🔎 Поиск фильмов'))
    kb.add(KeyboardButton('🎬 Тренды'), KeyboardButton('👻 Контакты'))
    kb.add(KeyboardButton('📊 Статистика'))
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


STATIC_TEXT_SPECIAL_HELP = """
🔎 Для поиска отправьте название фильма или сериала

📌 Также вы можете использовать следующие команды:
/popular - Популярные фильмы
/search_films - Поиск Фильмов
/contacts - Контакты
/statistics - Статистика
/help - Подсказки
"""

STATIC_TEXT_SPECIAL_HELP_ADMIN = """
👷🏻‍♂️ Вы являетесь админом бота. Для вас есть следующие команды:
/mailing - Рассылка сообщений пользователям    
"""

STATIC_TEXT_SPECIAL_START = """
Хеллоу, я Cinemoon 👻🤖 (Beta)

🔎 В моей библиотеке ты найдешь множество фильмов, сериалов и новинок киноиндустрии!

📌 Используй команду /help или нажми на кнопку 
"📕 Подсказки", чтобы узнать, как правильно пользоваться мной
"""

STATIC_TEXT_SPECIAL_SEARCH_FILMS = '🔎 Введите названия фильма и я покажу результаты поиска'

STATIC_TEXT_SPECIAL_CONTACTS = """
📝 Контакты
@iquzy - тех. поддержка, реклама 
"""

STATIC_BTN_HELP = btn_help()
