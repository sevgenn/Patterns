"""Модуль, содержащий описание запрашиваемых URL."""

from view import Home, About, Contacts, Admin, Courses, CreateCourse, CreateUser

urlpatterns = {
    '/': Home,
    '/about': About,
    '/contacts': Contacts,
    '/courses': Courses,
    '/admin': Admin,
    '/admin/create_course': CreateCourse,
    '/admin/create_user': CreateUser
}
