"""Модуль, содержащий описание запрашиваемых URL."""

from view import *

urlpatterns = {
    '/': Home,
    '/courses': Courses,
    '/about': About,
    '/contacts': Contacts,
    '/admin': Admin,
    '/admin/create_course': CreateCourse,
    '/admin/create_user': CreateUser,
    '/admin/students': Students,
    '/admin/add_to_course': AddToCourse,
    '/api/courses': ApiCourses,
}
