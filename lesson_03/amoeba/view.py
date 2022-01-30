"""Модуль пользовательских обработчиков."""

from amoeba.view import View
from amoeba.request import Request
from amoeba.response import Response
from amoeba.templator import render
from amoeba.storage_to_json import StorageManager


class Home(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'title': 'Home', 'bgcolor': 'cyan', 'session_id': request.session_id}
        body = render(request, 'home.html', **content)
        return Response(request, body=body)


class About(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        param1 = request.GET.get('param1')
        if not param1:
            param1 = '0'
        param2 = request.GET.get('param2')
        if not param2:
            param2 = '0'
        if param1 == '0' and param2 == '0':
            result = f'{param1} + {param2} = Nothing'
        else:
            result = f'{param1} + {param2} = Nothing anyway'
        content = {'title': 'About', 'bgcolor': 'darkcyan', 'result': result}
        body = render(request, 'about.html', **content)
        return Response(request, body=body)


class Contacts(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'title': 'Contacts', 'bgcolor': 'purple', 'client_name': 'GUEST'}
        body = render(request, 'contacts.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        name = request.POST.get('client_name')
        client_name = name if name else 'GUEST'
        topic = request.POST.get('topic')
        client_message = request.POST.get('client_message')
        client_email = request.POST.get('client_email')
        content = {'client_name': client_name, 'topic': topic, 'client_message': client_message,
                   'client_email': client_email}
        # Сохраняем сдоварь в json:
        StorageManager.add_to_json(request, 'messages.json', content)

        body = render(request, 'contacts.html', **content)
        return Response(request, body=body)
