import aiohttp
import re
from config import HDVD_TOKEN
from typing import List


class YaspellerResponse:
    uncorrect: str
    correct: str

    def __init__(self, uncorrect: str, correct: str):
        self.uncorrect = uncorrect
        self.correct = correct

    def __str__(self):
        return str({'uncorrect': self.uncorrect, 'correct': self.correct})


class Film:
    title: str
    iframe_url: str
    kinopoisk_id: int
    year: int
    quality: str
    poster: str

    def __init__(self, title: str, iframe_url: str, kinopoisk_id: int, year: int, quality: str, poster: str):
        self.title = title
        self.iframe_url = iframe_url
        self.kinopoisk_id = kinopoisk_id
        self.year = year
        self.quality = quality
        self.poster = poster

    def __str__(self):
        return str({
            'title': self.title,
            'iframe_url': self.iframe_url,
            'kinopoisk_id': self.kinopoisk_id,
            'year': self.year,
            'quality': self.quality,
            'poster': self.poster
        })


async def _yaspeller(title: str) -> List[YaspellerResponse]:
    u, p = 'https://speller.yandex.net/services/spellservice.json/checkText', {
        'lang': 'ru', 'text': title}
    async with aiohttp.ClientSession() as session:
        async with session.get(u, params=p) as resp:
            resp_json = await resp.json()
            return [YaspellerResponse(uncorrect=i['word'], correct=i['s'][0]) for i in resp_json]


def _sampling_films(films: list, film_title: str) -> List[List[int]]:
    """находит наибольшее кол-во совпадение в название фильма"""
    fts = re.split('\s|-|:|\.', film_title.lower().replace('ё', 'е'))
    len_fts, len_films = len(fts), len(films)

    result = [[] for _ in range(len_fts+1)]

    for film_index in range(len_films):
        f_title = re.split(
            '\s|-|:|\.', films[film_index]['title_ru'].lower().replace('ё', 'е'))

        k = 0
        for title_word in fts:
            if title_word in f_title:
                k += 1
        if k != 0:
            result[len_fts - k].append(film_index)

    return result


async def _sorted_films(films: List[Film]) -> List[Film]:
    """Сортировка фильмов по году выпуска"""
    return sorted(films, key=lambda film: film.year, reverse=True)


class HDVB:

    def __init__(self, token: str):
        self._token = token
        self._base_url = 'https://apivb.info/api/'

    async def find_by_title(self, title: str, limit: int = 25) -> List[Film]:
        films = []
        resp_json = await self._fetch('videos.json', title=title)

        if type(resp_json) == list and not resp_json:
            speller_check = await _yaspeller(title)
            for word in speller_check:
                title = title.replace(word.uncorrect, word.correct)
            resp_json = await self._fetch('videos.json', title=title)

        if type(resp_json) == list and resp_json:
            sort_films_index = _sampling_films(resp_json, title)

            k = 0
            kp_ids = {}

            for films_index in sort_films_index:
                for i in films_index:
                    if k >= limit:
                        return await _sorted_films(films)

                    if not kp_ids.get(resp_json[i]['kinopoisk_id']):
                        films.append(
                            Film(
                                title=resp_json[i]['title_ru'],
                                iframe_url=resp_json[i]['iframe_url'],
                                kinopoisk_id=resp_json[i]['kinopoisk_id'],
                                year=resp_json[i]['year'],
                                quality=resp_json[i]['quality'],
                                poster=resp_json[i]['poster'],
                            )
                        )
                        kp_ids[resp_json[i]['kinopoisk_id']] = 1
                        k += 1

        elif type(resp_json) == dict:
            print(resp_json)

        return await _sorted_films(films)

    async def _fetch(self, method: str, *args, **kwargs) -> dict:
        kwargs['token'] = self._token
        async with aiohttp.ClientSession() as session:
            async with session.get(self._base_url + method, params=kwargs) as resp:
                return await resp.json()


hdvb = HDVB(HDVD_TOKEN)
