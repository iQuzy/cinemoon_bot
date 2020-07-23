from aiogram.types import Message
from lib.handler import hl
from lib.hdvbDriver import hdvb
from lib.sortfilms import sort_index_compare
from lib.yaspeller import speller_check
import botkb


async def home_find(m: Message):
    hl.set_user_path('/films_search', m.from_user.id)
    await m.answer('Введите название фильма')


async def home_default(m: Message):
    await m.answer('Напишите "Поиск фильмов"')


async def films_search(m: Message):
    title = m.text
    await m.answer(f'Идёт поиск фильма "{title}"')

    films = hdvb.find_by_title(title)
    if not films:
        sp_check = speller_check(title)
        if sp_check:
            for i in sp_check:
                title = title.replace(i['uncorrect'], i['correct'])
            await m.answer(f'Возможно вы имели в виду "{title}"?')
            films = hdvb.find_by_title(title)

    sort = sort_index_compare(films, title)

    k = 0
    k_max = 50
    film_kp_ids = {}

    for sort_films_index in sort:
        for film_index in sort_films_index:
            if k >= k_max:
                return
            if film_kp_ids.get(films[film_index]['kinopoisk_id']):
                continue

            f = films[film_index]
            film_kp_ids[f['kinopoisk_id']] = True
            caption = f"🎬 {f['title_ru']} ({str(f['year']) + '/' if f['year'] else ''}{f['quality']})"

            await m.answer_photo(f['poster'], caption=caption, reply_markup=botkb.search_film(f['iframe_url'], f['kinopoisk_id']))
            k += 1

    if k == 0:
        await m.answer("Простите, я ничего не нашел")


async def specil_home(m: Message):
    hl.set_user_path('/', m.from_user.id)
    await m.answer('Вы вернулись домой')
