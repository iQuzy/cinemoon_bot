import re


def distance(a: str, b: str):
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n

    current_row = range(n + 1)
    for i in range(1, m + 1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n + 1):
            add, delete, change = previous_row[j] + \
                1, current_row[j - 1] + 1, previous_row[j - 1]
            if a[j - 1] != b[i - 1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]


def sort_index(films: list, film_title: str):
    ftl = len(film_title)
    max_distance = 20 if ftl > 20 else ftl**2

    _md = max_distance - 1
    result = [[] for _ in range(max_distance)]
    film_title_lower = film_title.lower()

    l = len(films)

    for i in range(l):
        d = distance(films[i]['title_ru'].lower(), film_title_lower)

        if d <= _md:
            result[d].append(i)

    return result


def sort_index_compare(films: list, film_title: str):
    fts = re.split('\s|-|:|\.', film_title.lower().replace('ё', 'е'))
    len_fts = len(fts)
    len_films = len(films)

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
