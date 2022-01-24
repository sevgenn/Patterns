"""Модуль, содержащий описание запрашиваемых URL."""

from view import Home, About, Contacts

urlpatterns = {
    '/': Home,
    '/about': About,
    '/contacts': Contacts
}
