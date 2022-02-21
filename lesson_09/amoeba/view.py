"""Модуль пользовательских обработчиков."""

import re
from amoeba.view import View
from amoeba.request import Request
from amoeba.response import Response
from amoeba.templator import render
from amoeba.router import Router
from amoeba.storage_to_json import StorageManager
from models.site_models import Site
from models.logger import Logger, WriterToConsole, WriterToFile
from models.debuger import DebugDecorator
from models.get_json import CoursesToJson
from patterns.domain import UnitOfWork
from models.datamapper import MapperRegistry, CategoryMapper, connection

routes = {}

console_writer = WriterToConsole()
file_writer = WriterToFile('vew')
logger = Logger('view')
logger.writer = console_writer

site = Site()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

#######################################################
# Тестовые присвоения:
# try:
#     new_cat1 = site.create_course_category('programming')
#     new_cat1.mark_new()
#     new_cat2 = site.create_course_category('web', new_cat1)
#     new_cat2.mark_new()
#     new_cat3 = site.create_course_category('python', new_cat2)
#     new_cat1.mark_new()
#
#     new_course1 = site.create_course('online', 'django', new_cat3)
#     new_course1.mark_new()
#     new_course2 = site.create_course('online', 'flask', new_cat3)
#     new_course2.mark_new()
#     new_course3 = site.create_course('online', 'php', new_cat2)
#     new_course3.mark_new()
#
#     new_student1 = site.create_user('student', 'Sam')
#     new_student1.mark_new()
#     new_student2 = site.create_user('student', 'Bob')
#     new_student2.mark_new()
#     new_student3 = site.create_user('student', 'Pit')
#     new_student3.mark_new()
#
#     UnitOfWork.get_current().commit()
# except Exception as err:
#     print('Error: ', err.args)
#######################################################

@Router(routes, '/')
@DebugDecorator()
class Home(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = {'bgcolor': 'cyan', 'session_id': request.session_id}
        body = render(request, 'home.html', **content)
        logger.log('class Home')
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
        logger.log('class Contacts')
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
        category = site.get_category_by_name(course_category)
        new_course = site.create_course(course_type, course_name, category)
        new_course.mark_new()
        UnitOfWork.get_current().commit()

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
        if user_category and user_name:
            # Добавляется новый объект класса User:
            new_user = site.create_user(user_category, user_name)
            new_user.mark_new()
            UnitOfWork.get_current().commit()
        body = render(request, 'create_user.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/existing_categories')
@DebugDecorator()
class ExistingCategories(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories_list = [item for item in site.get_categories()]
        content = {
            'categories_list': categories_list
        }
        body = render(request, 'existing_categories.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        upper_category = request.POST.get('upper_category')
        content = {
            'upper_category': upper_category
        }
        body = render(request, 'create_category.html', **content)
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
        new_category = site.create_course_category(category_name, parent_object)
        new_category.mark_new()
        UnitOfWork.get_current().commit()

        body = render(request, 'create_category.html', **content)
        return Response(request, body=body)


###############################  NEW ######################################


@Router(routes, '/courses')
@DebugDecorator()
class Courses(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        categories_list = [item for item in site.get_categories()]
        content = {
            'categories_list': categories_list
        }
        body = render(request, 'courses.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/students')
@DebugDecorator()
class Students(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        students_list = [(item, item.studied_courses) for item in site.get_students()]
        content = {
            'students_list': students_list
        }
        body = render(request, 'students.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/add_to_course')
@DebugDecorator()
class AddToCourse(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        courses_list = site.get_courses()
        students_list = site.get_students()
        content = {
            'courses_list': courses_list,
            'students_list': students_list
        }
        body = render(request, 'add_to_course.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.POST
        course_name = data.get('course_name')
        student_name = data.get('student_name')
        regex = re.compile('[\W]*[\w]+')
        if regex.match(course_name) and regex.match(student_name):
            student = site.get_student_by_name(student_name)
            course = site.get_course_by_name(course_name)
            student.add_studied_courses(course)
        courses_list = site.get_courses()
        students_list = site.get_students()
        content = {
            'courses_list': courses_list,
            'students_list': students_list
        }
        body = render(request, 'add_to_course.html', **content)
        return Response(request, body=body)


@Router(routes, '/api/courses')
@DebugDecorator()
class ApiCourses(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        content = CoursesToJson(site).get_json()
        return Response(request, body=content)


@Router(routes, '/admin/existing_courses')
@DebugDecorator()
class ExistingCourses(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        courses_list = [item for item in site.get_courses()]
        content = {
            'courses_list': courses_list
        }
        body = render(request, 'existing_courses.html', **content)
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        existing_course_name = request.POST.get('existing_course')
        existing_course = site.get_course_by_name(existing_course_name)
        new_course = existing_course.clone()
        site.add_course(new_course)

        content ={
            'course': new_course
        }

        body = render(request, 'edit_course.html', **content)
        return Response(request, body=body)


@Router(routes, '/admin/course')
@DebugDecorator()
class EditCourse(View):
    def get(self, request: Request, *args, **kwargs) -> Response:
        body = render(request, 'edit_course.html')
        return Response(request, body=body)

    def post(self, request: Request, *args, **kwargs) -> Response:
        course = site.get_course_by_name('name')
        print(course.name)
        data = request.POST.get()
        course.name = data['name']
        course.parent = data['category_name']

        body = render(request, 'existing_courses.html')
        return Response(request, body=body)
