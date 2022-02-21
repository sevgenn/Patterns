"""Модуль, обрабатывающий все входящие запросы (Front controller)."""

from uuid import uuid4
from urllib.parse import parse_qs
from amoeba.request import Request
from amoeba.response import Response


class BaseController:
    """Базовый класс контроллеров."""

    def to_request(self, request: Request):
        return

    def to_response(self, response: Response):
        return


class Session(BaseController):
    """Класс, передающий cookie клиенту."""

    def to_request(self, request: Request):
        cookie = request.environ.get('HTTP_COOKIE', None)
        # print('COOKIE: ', cookie)
        if not cookie:
            return
        # session_id = parse_qs(cookie)['session_id'][0]
        session_id = cookie.split(' ')[1].split('=')[1]
        # print('SESSION_ID: ', session_id)
        request.extras['session_id'] = session_id

    def to_response(self, response: Response):
        """Передает session ID в заголовки Response."""
        if not response.request.session_id:
            response.update_headers(
                {'Set-Cookie': f'session_id={uuid4()}'}
            )


front_controllers = [
    Session
]
