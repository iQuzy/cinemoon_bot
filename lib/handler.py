import sqlite3
import re
from aiogram.types import Message, CallbackQuery
from typing import List


class Handler:
    def __init__(self, dbpath: str):
        # database
        self._db = self._Database(dbpath)

        # база обработчиков
        self._handlers_array = {}
        self._handlers_array['special'] = []
        self._query_handler_array = []

    async def handle_message(self, m: Message) -> None:
        """обработчик входящих сообщений"""
        user_path = self._db.get_user_path(m.from_user.id)
        m.text = '' if not m.text else m.text

        async def search_handler(_message: str, _handlers):
            _handlers = _handlers[0]
            for handler in _handlers:
                if re.match(handler[0], _message):
                    return handler[1]
            return None

        func = await search_handler(m.text, self._handlers_array['special'])
        if func:
            await func(m)
            return

        handlers = self._handlers_array.get(user_path)
        if handlers:
            func = await search_handler(m.text, handlers)
            if func:
                await func(m)
                return

    async def handle_query(self, c: CallbackQuery) -> None:
        """обработчик callback запросов"""
        for query in self._query_handler_array:
            await query[1](c) if re.match(query[0], c.data) else 0

    def add(self, action_path: str, templates: dict) -> None:
        """добавить обработчик сообщений"""
        if not (self._handlers_array.get(action_path)):
            self._handlers_array[action_path] = []
        self._handlers_array[action_path].append(list(templates.items()))

    def add_query(self, template: str, func) -> None:
        """добавить обработчик callback запросов"""
        self._query_handler_array.append([template, func])

    def get_user_path(self, user_id: int) -> str:
        return self._db.get_user_path(user_id)

    def set_user_path(self, new_path: str, user_id: int) -> None:
        return self._db.set_user_path(new_path, user_id)

    def get_all_ids(self) -> List[int]:
        ids = self._db.get_all_ids()
        return [i[0] for i in ids]

    class _Database:

        def __init__(self, dbpath: str):
            self._connect = sqlite3.connect(dbpath)
            self._cursor = self._connect.cursor()
            self._init_db()

        def _init_db(self) -> None:
            self._cursor.execute(
                'CREATE TABLE IF NOT EXISTS "users" (' +
                '"tg_id" INTEGER NOT NULL UNIQUE,' +
                '"path" TEXT NOT NULL DEFAULT "/",' +
                'PRIMARY KEY("tg_id"));'
            )
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

        def get_all_ids(self) -> List[List[int]]:
            return self._cursor.execute('SELECT "tg_id" FROM "main"."users"').fetchall()