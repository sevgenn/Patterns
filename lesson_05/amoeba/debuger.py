"""Модуль, содержащий декоратор для логирования запуска функции."""

from time import time
from functools import wraps


class DebugDecorator:
    """Логгер-декоратор, информирующий о запуске функции."""

    def __call__(self, view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            start_time = time()
            result = view(*args, **kwargs)
            delta = time() - start_time
            print(f'DEBUG <==> object {view.__name__} performed {delta:.8f} c')

            return result
        return wrapper
