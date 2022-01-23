"""Модуль, описывающий ошибки."""

from amoeba.templator import render
from amoeba.request import Request
from amoeba.view import View


class NotFoundPage(View):
    """Вьюха, формирующая страницу NotFound."""

    def get(self, request: Request, *args, **kwargs):
        body = render(request, 'not_found.html', **{'err': 'Not Found', 'text': 'Page Not Found!'})
        return '404 Not Found', body
