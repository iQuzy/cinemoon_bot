from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def search_film(iframe_url: str, kinopoisk_id: int):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('🍿Смотреть фильм', url=iframe_url))
    kb.add(InlineKeyboardButton('📙КиноПоиск', url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'))
    return kb