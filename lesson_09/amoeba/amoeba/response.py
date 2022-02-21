"""Модуль ответов сервера."""

from amoeba.request import Request


class Response:
    """Класс ответов."""

    def __init__(self, request: Request, status_code: int = 200, headers: dict = None, body: str = ''):
        self.request = request
        self.status_code = status_code
        self.headers = {}
        self.body = b''
        self._set_base_headers()
        if headers is not None:
            self.update_headers(headers)
        self._set_body(body)
        self.extras = {}

    def __getattr__(self, item):
        """Позволяет возвращать вызываемые параметры."""
        return self.extras.get(item)

    def _set_base_headers(self):
        """Устанавливает заголовки по умолчанию."""
        self.headers = {
            'Content-Type': 'text/html',
            'Content-Length': 0
        }

    def update_headers(self, headers: dict):
        """Обновляет заголовки."""
        self.headers.update(headers)

    def _set_body(self, raw_body: str):
        self.body = raw_body.encode('utf-8')
        self.update_headers(
            {'Content-Length': str(len(self.body))}
        )
