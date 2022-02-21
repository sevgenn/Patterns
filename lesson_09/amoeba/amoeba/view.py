"""Модуль контроллеров."""

from amoeba.request import Request
from amoeba.response import Response


class View:
    """Базовый класс Page-контроллеров."""

    def get(self, request: Request, *args, **kwargs) -> Response:
        pass

    def post(self, request: Request, *args, **kwargs) -> Response:
        pass
