import requests as rqs

def speller_check(film_title):
    r = rqs.get('https://speller.yandex.net/services/spellservice.json/checkText', params={
        'lang': 'ru',
        'text': film_title
    }).json()

    
    return [{'uncorrect': i['word'], 'correct': i['s'][0]} for i in r]
