"""Модуль обработки представлений."""

class Router:
    """
    Декоратор класса-представления.
    Назначает соответствие между url и объектом класса View.
    """
    def __init__(self, routes: dict, url: str = ''):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        self.routes[self.url] = cls
