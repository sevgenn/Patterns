"""Основной модуль, определяющий точку входа и логику приложения."""

from typing import List, Type
from amoeba.view import View
from amoeba.error_view import NotFoundPage
from amoeba.exceptions import NotAllowed
from amoeba.request import Request
from amoeba.response import Response
from amoeba.fronts import BaseController


class Amoeba:
    """Основной класс приложения."""

    def __init__(self, routes: dict, settings: dict, fronts: List[Type[BaseController]]):
        self.routes = routes
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

    def _process_url(self, url: str) -> str:
        """Обрабатывает слэш в конце адреса."""
        if len(url) > 1:
            if url[-1] == '/':
                return url[:-1]
        return url

    def _find_view(self, raw_url: str) -> Type[View]:
        """Ищет соответствующую адресу вьюху."""
        url = self._process_url(raw_url)
        if url in self.routes:
            return self.routes[url]
        return NotFoundPage

    def _get_view(self, environ: dict) -> View:
        """Инициализирует соответствующую адресу вьюху."""
        raw_url = environ['PATH_INFO']
        view = self._find_view(raw_url)
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

    def router(self, url: str):
        def wrapper(view):
            self.routes[url] = view
            return view
        return wrapper


class FakeApplication(Amoeba):
    """Класс-фейк, выдающий одну и ту же информацию."""
    def __init__(self, routes: dict, settings: dict, fronts: List[Type[BaseController]]):
        self.app = Amoeba(routes, settings, fronts)
        super().__init__(routes, settings, fronts)

    def __call__(self, environ: dict, start_response):
        start_response('200 OK', [('Content_Type', 'text/html')])
        return [b'Hello from Fake']


class LogApplication(Amoeba):
    """Класс-логгер, выдающий для каждого запроса его тип и параметры."""
    def __init__(self, routes: dict, settings: dict, fronts: List[Type[BaseController]]):
        self.app = Amoeba(routes, settings, fronts)
        super().__init__(routes, settings, fronts)

    def __call__(self, environ: dict, start_response):
        print(f"LOG <==> REQUEST_METHOD: {environ['REQUEST_METHOD']}\n"
              f"LOG <==> QUERY_STRING: {environ['QUERY_STRING']}\n"
              f"LOG <==> wsgi.input: {environ['wsgi.input'].read().decode('utf-8')}")
        return self.app(environ, start_response)
