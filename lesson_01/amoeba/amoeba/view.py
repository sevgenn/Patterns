"""Модуль контроллеров."""

from amoeba.request import Request


class View:
    """Базовый класс Page-контроллеров."""

    def get(self, request: Request, *args, **kwargs):
        pass

    def post(self, request: Request, *args, **kwargs):
        pass
