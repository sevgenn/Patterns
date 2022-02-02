"""
Модуль логирования.
В режиме DEBUG (задается в settings) сохраняет логи вызываемых функций в соответствующие файлы.
"""

import os
from datetime import datetime
from settings import settings
from patterns.singletones import Singletone


class Logger(metaclass=Singletone):
    """Класс-логгер."""

    def log(self, name, text=''):
        """Записывает логи в файл."""
        if settings.get('DEBUG') == True:
            log_path = self.create_log_dir(name)
            with open(log_path, 'a') as file_write:
                file_write.write(text + '\n')
        else:
            pass

    def create_log_dir(self, name) -> str:
        """Возвращает путь до файла-логов."""
        log_dir = os.path.join(settings.get('BASE_DIR'), settings.get('LOG_DIR'))
        log_name = f'{name}.log'
        return os.path.join(log_dir, log_name)


class LogDecorator:
    """Логгер-декоратор."""

    def __init__(self, logger):
        self.logger = logger

    def __call__(self, func_to_log):
        def wrapper(*args, **kwargs):
            result = func_to_log(*args, **kwargs)
            self.logger.log(name=f'{func_to_log.__module__}',
                            text=f'{datetime.now()} <==> '
                                 f'module: {func_to_log.__module__} || '
                                 f'function: {func_to_log.__name__} ')
            return result
        return wrapper


if __name__ == '__main__':
    logger1 = Logger()
    logger2 = Logger()
    print(logger1 is logger2)
