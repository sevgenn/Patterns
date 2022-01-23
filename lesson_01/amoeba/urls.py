"""Модуль, содержащий описание запрашиваемых URL."""

from view import Home, About

urlpatterns = {
    '/': Home,
    '/about': About
}
