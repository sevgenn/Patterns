"""Модуль пользовательских обработчиков."""

from amoeba.view import View
from amoeba.request import Request
from amoeba.templator import render


class Home(View):
    def get(self, request: Request, *args, **kwargs):
        body = render(request, 'home.html', **{'session_id': request.session_id})
        return '200 OK', body


class About(View):
    def get(self, request: Request, *args, **kwargs):
        body = render(request, 'about.html')
        return '200 OK', body
