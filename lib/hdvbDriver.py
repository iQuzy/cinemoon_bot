import requests as rqs
from config import HDVD_TOKEN


class HDVB:

    def __init__(self, token: str):
        self._token = token
        self._base_url = 'https://apivb.info/api/'

    def find_by_title(self, title: str) -> list:
        res = self._fetch('videos.json', title=title)
        return res

    def _fetch(self, method: str, *args, **kwargs) -> dict:
        kwargs['token'] = self._token
        return rqs.get(self._base_url + method, params=kwargs).json()

hdvb = HDVB(HDVD_TOKEN)