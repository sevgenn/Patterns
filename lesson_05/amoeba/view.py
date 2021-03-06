"""Модуль пользовательских обработчиков."""

from amoeba.view import View
from amoeba.request import Request
from amoeba.response import Response
from amoeba.templator import render
from amoeba.router import Router
from amoeba.storage_to_json import StorageManager
from models.site_models import Site
from logger import Logger
from debuger import DebugDecorator

logger = Logger('view')
site = Site()
routes = {}

# Тестовые присвоения:
cat1 = site.create_course_category('programming')
cat2 = site.create_course_category('web', cat1)
cat3 = site.create_course_category('python', cat2)
course1 = site.create_course('online', 'django', cat3)
course2 = site.create_course('online', 'flask', cat3)
course3 = site.create_course('online', 'php', cat2)


@Router(routes, '/')
@DebugDecorator()
class Home(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'bgcolor': 'cyan', 'session_id': request.session_id}
        body = render(request, 'home.html', **content)
        logger.log()
        return Response(request, body=body)


@Router(routes, '/about')
@DebugDecorator()
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
        content = {'bgcolor': 'darkcyan', 'result': result}
        body = render(request, 'about.html', **content)
        return Response(request, body=body)


@Router(routes, '/contacts')
@DebugDecorator()
class Contacts(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'bgcolor': 'purple', 'client_name': 'GUEST'}
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

@Router(routes, '/admin')
@DebugDecorator()
class Admin(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, 'admin.html')
        return Response(request, body=body)


@Router(routes, '/admin/create_course')
@DebugDecorator()
class CreateCourse(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, 'create_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        # print(request.POST)
        content = request.POST
        course_type = content.get('course_type')
        course_category = content.get('course_category')
        course_name = content.get('course_name')
        # Добавляется новый объект класса Course:
        site.create_course(course_type, course_name, course_category)
        # Запись в json-файл:
        file_name = 'courses.json'
        StorageManager.add_to_json(request, file_name, content)

        body = render(request, 'create_course.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/create_user')
@DebugDecorator()
class CreateUser(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, 'create_user.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        content = request.POST
        user_category = content.get('user_category')
        user_name = content.get('user_name')
        # Добавляется новый объект класса User:
        site.create_user(user_category, user_name)
        # Запись в json-файл:
        file_name = user_category + 's.json'
        StorageManager.add_to_json(request, file_name, content)
        body = render(request, 'create_user.html', **content)
        return Response(request, body=body)


@Router(routes, '/courses')
@DebugDecorator()
class Courses(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories_list = [(item, item.courses) for item in site.get_categories()]
        content = {
            'categories_list': categories_list
        }

        body = render(request, 'courses.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/existing_categories')
@DebugDecorator()
class ExistingCategories(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories_list = [(item.name, item.id) for item in site.get_categories()]
        content = {
            'categories_list': categories_list
        }
        body = render(request, 'existing_categories.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/create_category')
@DebugDecorator()
class CreateCategory(View):
    def get(self, request: Request, *args, **kwargs) -> Response:

        body = render(request, 'create_category.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        content = request.POST
        parent_name = content.get('parent_category')
        parent_object = site.get_category_by_name(parent_name)
        category_name = content.get('category_name')
        # Добавляется новый объект класса CourseCategory:
        site.create_course_category(category_name, parent_object)

        body = render(request, 'create_category.html', **content)
        return Response(request, body=body)
