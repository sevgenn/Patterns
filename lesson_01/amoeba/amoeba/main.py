"""Основной модуль, определяющий точку входа и логику приложения."""

from typing import List, Type
from amoeba.view import View
from amoeba.exceptions import NotFoundPage
from amoeba.request import Request
from amoeba.fronts import BaseController


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
        # Запускаем Front-controller:
        self._get_fronts(request)
        code, raw_body = view.get(request)
        body = raw_body.encode('utf-8')
        start_response(code, [('Content-Type', 'text/html'), ('Content-Length', str(len(body)))])
        return iter([body])

    def _process_url(self, url: str) -> str:
        """Обрабатывает слэш в конце адреса."""
        if len(url) > 1:
            if url[-1] == '/':
                return url[:-1]
        return url

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
        return view()

    def _get_request(self, environ: dict) -> Request:
        """Возвращает объект запроса."""
        return Request(environ, self.settings)

    def _get_fronts(self, request: Request):
        """Запускает Front-контроллеры."""
        for front in self.fronts:
            front().to_request(request)
