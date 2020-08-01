import sqlite3
import re
from aiogram import types
import typing

class Handler:

    def __init__(self, dbpath: str):
        self._connect = sqlite3.connect(dbpath)
        self._cursor = self._connect.cursor()

        self._base_init()

        self._handlers_array = {}
        self._handlers_array['special'] = []

        self.query_handler_array = []

    def _base_init(self):
        self._cursor.execute(
            'CREATE TABLE IF NOT EXISTS "users" ("tg_id" INTEGER NOT NULL UNIQUE, "path" TEXT NOT NULL DEFAULT "/", PRIMARY KEY("tg_id"));')
        self._connect.commit()

    def get_user_path(self, user_id: int) -> str:
        u = self._cursor.execute(
            'SELECT "path" FROM "main"."users" WHERE tg_id = ?;', (user_id,)).fetchone()
        if u:
            return u[0]
        else:
            self._cursor.execute(
                'INSERT INTO "main"."users" ("tg_id") VALUES (?);', (user_id,))
            self._connect.commit()
            return '/'

    def set_user_path(self, new_path: str, user_id: int) -> None:
        self._cursor.execute(
            'UPDATE "main"."users" SET path = (?) WHERE tg_id = (?);', (new_path, user_id))
        self._connect.commit()

    def get_all_ids(self) -> typing.List:
        return self._cursor.execute('SELECT "tg_id" FROM "main"."users"').fetchall()

    # обработчик входящих сообщений
    async def handle_message(self, m: types.Message) -> None:
        user_path = self.get_user_path(m.from_user.id)
        m.text = '' if not m.text else m.text
    
        def search_handler(_message: str, _handlers):
            _handlers = _handlers[0]
            for handler in _handlers:
                if re.match(handler[0], _message):
                    return handler[1]
            return None

        func = search_handler(m.text, self._handlers_array['special'])
        if func:
            await func(m)
            return

        h = self._handlers_array.get(user_path)
        if h:
            func = search_handler(m.text, h)
            if func:
                await func(m)
                return

    async def handle_query(self, c: types.CallbackQuery) -> None:
        for i in self.query_handler_array:
            await i[1](c) if re.match(i[0], c.data) else 0

    def add(self, path: str, templates: dict) -> None:
        if not (self._handlers_array.get(path)):
            self._handlers_array[path] = []
        self._handlers_array[path].append(list(templates.items()))

    def add_query(self, template: str, func) -> None:
        self.query_handler_array.append([template, func])



