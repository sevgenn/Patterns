"""Модуль, обрабатывающий все входящие запросы (Front controller)."""

from urllib.parse import parse_qs
from amoeba.request import Request


class BaseController:
    """Базовый класс контроллеров."""

    def to_request(self, request: Request):
        return


class Session(BaseController):
    """Класс, передающий cookie клиента в запрос."""

    def to_request(self, request: Request):
        cookie = request.environ.get('HTTP_COOKIE', None)
        # print('COOKIE ', cookie)
        if not cookie:
            return
        session_id = parse_qs(cookie)['session_id'][0]
        # print('SESSION_ID ', session_id)
        request.extras['session_id'] = session_id


front_controllers = [
    Session
]
