from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton


def help():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📕 Подсказки"))
    return kb


def search_film(iframe_url: str, kinopoisk_id: int, watch_btn=False):
    kb = InlineKeyboardMarkup()

    if watch_btn:
        kb.add(InlineKeyboardButton('🍿 Смотреть онлайн',
                                    url=f'https://iquzy.github.io/cm?f={iframe_url}'))
    else:
        kb.add(InlineKeyboardButton('🔮 Кнопка для просмотра', callback_data=f'show_watch_btn|{kinopoisk_id}'))

    kb.add(InlineKeyboardButton('📙 Подробнее на КиноПоиск',
                                url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'))
    return kb


static_help = help()
