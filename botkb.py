from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def back_home():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("💃 Назад"))
    return kb

def search_film(iframe_url: str, kinopoisk_id: int, btn_info=True):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton('🍿Смотреть фильм', url=f'https://iquzy.github.io/cm?f={iframe_url}'))
    kb.add(InlineKeyboardButton('📙Подробнее на Кинопоиске', url=f'https://www.kinopoisk.ru/film/{kinopoisk_id}'))
    return kb

static_back_home = back_home()