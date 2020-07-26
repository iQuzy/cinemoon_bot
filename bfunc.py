from aiogram.types import Message, CallbackQuery
from lib.handler import hl
from lib.hdvbDriver import hdvb
import botkb


async def home_find(m: Message):
    hl.set_user_path('/search_films', m.from_user.id)
    await m.answer('Введите название фильма', reply_markup=botkb.static_back_home)


async def home_default(m: Message):
    await m.answer('Используйте команту \n/search_films для посика фильмов')


async def search_films(m: Message):
    await m.answer(f'Идёт поиск фильма "{m.text}"')

    films = await hdvb.find_by_title(m.text, limit=25)

    if films:
        for film in films:
            caption = "🎬{title} ({year}{quality})".format(
                title=film.title,
                year=str(film.year) + '/' if film.year else '',
                quality=film.quality
            )
            await m.answer_photo(film.poster, caption=caption, reply_markup=botkb.search_film(film.iframe_url, film.kinopoisk_id))
    else:
        await m.answer("Простите, я ничего не нашел")
    del films

async def specil_home(m: Message):
    hl.set_user_path('/', m.from_user.id)
    await m.answer('Вы вернулись домой 💃')

# async def query_film_info(c: CallbackQuery):
#     await c.answer('Получение информации о фильме..')
#     kinopoisk_id =  re.search('\d+', c.data).group(0)
#     hdvb.get_film_info(kinopoisk_id)
