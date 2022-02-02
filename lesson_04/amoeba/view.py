"""Модуль пользовательских обработчиков."""

from amoeba.view import View
from amoeba.request import Request
from amoeba.response import Response
from amoeba.templator import render
from amoeba.storage_to_json import StorageManager
from models.courses_models import CourseFactory
from models.users_models import *
from models.site_models import Site
from logger import Logger, LogDecorator

logger = Logger()
site = Site()


@LogDecorator(logger)
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

#####################################   NEW   #############################################

class Admin(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'title': 'Admin'}
        body = render(request, 'admin.html', **content)
        return Response(request, body=body)


class CreateCourse(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'title': 'Admin'}
        body = render(request, 'create_course.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        # print(request.POST)
        course_category = request.POST.get('course_category')
        course_name = request.POST.get('course_name')
        new_course = CourseFactory.create_course(course_category, course_name)
        # Добавляется новый класс-курс
        site.add_course(new_course)
        content = request.POST
        # Запись в json-файл:
        file_name = 'courses.json'
        StorageManager.add_to_json(request, file_name, content)

        body = render(request, 'create_course.html', **content)
        return Response(request, body=body)


class CreateUser(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'title': 'Admin'}
        body = render(request, 'create_user.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        user_category = request.POST.get('user_category')
        user_name = request.POST.get('user_name')
        user_creator = UserFactory.create_user(user_category)
        # Добавляется новый класс-user:
        if user_category == 'teacher':
            new_user = user_creator.create_teacher(user_name)
            site.add_teacher(new_user)
        elif user_category == 'student':
            new_user = user_creator.create_student(user_name)
            site.add_student(new_user)
        else:
            Response.status_code = 400
        content = request.POST
        # Запись в json-файл:
        file_name = user_category + 's.json'
        StorageManager.add_to_json(request, file_name, content)

        body = render(request, 'create_user.html', **content)
        return Response(request, body=body)


class Courses(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        course_list = []
        courses = StorageManager.get_from_json(request, 'courses.json')
        # print(courses_list)
        for item in courses:
            course_list.append(item['course_name'])
        content = {'title': 'Courses', 'course_list': course_list}

        body = render(request, 'courses.html', **content)
        return Response(request, body=body)

