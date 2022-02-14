"""Модуль, описывающий ошибки."""

from jinja2 import Template
from amoeba.request import Request
from amoeba.response import Response
from amoeba.view import View


class NotFoundPage(View):
    """Вьюха, формирующая страницу NotFound."""

    def get(self, request: Request, *args, **kwargs):
        content = {
            'err': 'Not Found',
            'text': '"404"',
            'comment': 'The requested page is not found or has never existed. Try to get backwards.'
        }
        with open('amoeba/templates/not_found.html', encoding='utf-8') as f:
            template = Template(f.read())

        body = template.render(**content)
        return Response(request, body=body)
