"""Модуль исключений."""


class NotFound(Exception):
    """Класс-исключение для отсутствующей страницы."""
    code = 404
    text = 'Page not found'


class NotAllowed(Exception):
    """Класс-исключение для недопустимого метода."""
    code = 405
    text = 'Method HTTP not allowed'


class BadRequest(Exception):
    """Класс-исключени для неверного синтаксиса запроса."""
    code = 400
    text = 'Bad Request'
