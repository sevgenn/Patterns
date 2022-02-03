"""
Модуль логирования.
В режиме DEBUG (задается в settings) сохраняет логи вызываемых функций в соответствующие файлы.
"""

import os
import traceback
from datetime import datetime
from settings import settings
from patterns.singletones import Singletone


class Writer:
    def __init__(self, path: str):
        self.path = path

    def write(self, text: str):
        with open(self.path, 'a') as file_write:
            file_write.write(text + '\n')


class Logger(metaclass=Singletone):
    """Класс-логгер."""
    def __init__(self, name: str):
        self.name = name
        path = self.create_log_dir()
        self.writer = Writer(path)

    def log(self, text: str=''):
        """Записывает логи в файл."""
        if settings.get('DEBUG') == True:
            if not text:
                text = f'logging function {traceback.extract_stack()[-2][2]}'
            data = f'log <==> {datetime.now()} <==> {text}'
            self.writer.write(data)
        else:
            pass

    def create_log_dir(self) -> str:
        """Возвращает путь до файла-логов."""
        log_dir = os.path.join(settings.get('BASE_DIR'), settings.get('LOG_DIR'))
        log_name = f'{self.name}.log'
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
    logger1 = Logger('main')
    logger2 = Logger('second')
    logger3 = Logger('main')
    print(logger1 is logger2)
    print(logger1 is logger3)

    print(traceback.extract_stack()[-1][2])
