"""Основной модуль, определяющий точку входа и логику приложения."""

from typing import List, Type
from amoeba.view import View
from amoeba.error_view import NotFoundPage
from amoeba.exceptions import NotAllowed
from amoeba.request import Request
from amoeba.response import Response
from amoeba.fronts import BaseController
from logger import Logger, LogDecorator

logger = Logger('main')

class Amoeba:
    """Основной класс приложения."""

    def __init__(self, urls: dict, settings: dict, fronts: List[Type[BaseController]]):
        self.urls = urls
        self.settings = settings
        self.fronts = fronts

    def __call__(self, environ: dict, start_response):
        # Формируем request:
        request = self._get_request(environ)
        # Получаем вьюху:
        view = self._get_view(environ)
        # Передаем параметры Front-controller в request:
        self._get_fronts_request(request)
        # Получаем response:
        response = self._get_response(environ, view, request)
        # Передаем параметры Front-controller в response:
        self._get_fronts_response(response)
        start_response(str(response.status_code), response.headers.items())
        return iter([response.body])

    @LogDecorator(logger)
    def _process_url(self, url: str) -> str:
        """Обрабатывает слэш в конце адреса."""
        if len(url) > 1:
            if url[-1] == '/':
                return url[:-1]
        return url

    @LogDecorator(logger)
    def _find_view(self, raw_url: str) -> Type[View]:
        """Ищет соответствующую адресу вьюху."""
        url = self._process_url(raw_url)
        if url in self.urls:
            return self.urls[url]
        return NotFoundPage

    def _get_view(self, environ: dict) -> View:
        """Инициализирует соответствующую адресу вьюху."""
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)
        logger.log()
        return view()

    def _get_request(self, environ: dict) -> Request:
        """Возвращает объект запроса."""
        return Request(environ, self.settings)

    def _get_response(self, environ: dict, view: View, request: Request) -> Response:
        """Возвращает объект ответа."""
        method = environ['REQUEST_METHOD'].lower()
        # print('METHOD ', method)
        # print(hasattr(view, method))
        if not hasattr(view, method):
            raise NotAllowed
        # Получаем атрибуты класса, вызываем функцию и передаем ей request:
        return getattr(view, method)(request)

    def _get_fronts_request(self, request: Request):
        """Передает в request параметры Front-контроллера."""
        for front in self.fronts:
            front().to_request(request)

    def _get_fronts_response(self, response: Response):
        """Передает в response параметры Front-контроллера."""
        for front in self.fronts:
            front().to_response(response)
