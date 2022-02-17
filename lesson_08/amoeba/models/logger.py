"""
Модуль логирования.
В режиме DEBUG (задается в settings) записывает логи вызываемых функций в соответствии с выбранным методом
(консоль или ффайл).
"""

from abc import ABC, abstractmethod
import os
import traceback
from datetime import datetime
from typing import Type

from settings import settings
from patterns.singletones import Singletone


class AbstractWriter(ABC):
    @abstractmethod
    def write(self, text: str):
        pass


class WriterToFile(AbstractWriter):
    """Класс, выводящий запись в файл."""
    def __init__(self, logger_name: str):
        self.name = logger_name
        self.path = self.create_log_dir()

    def create_log_dir(self) -> str:
        """Возвращает путь до файла-логов."""
        log_dir = os.path.join(settings.get('BASE_DIR'), settings.get('LOG_DIR'))
        log_name = f'{self.name}.log'
        return os.path.join(log_dir, log_name)

    def write(self, text: str) -> None:
        with open(self.path, 'a') as file_write:
            file_write.write(text + '\n')


class WriterToConsole(AbstractWriter):
    """Класс, выводящий запись в консоль."""
    def write(self, text: str) -> None:
        print(text)


class Logger(metaclass=Singletone):
    """Класс-логгер."""
    def __init__(self, name: str, writer=None):
        self.name = name
        self._writer = writer

    @property
    def writer(self) -> Type[AbstractWriter]:
        return self._writer

    @writer.setter
    def writer(self, writer: Type[AbstractWriter]):
        """Позволяет выбрать writer при конкретном вызове."""
        self._writer = writer

    def log(self, data):
        """Записывает логи в соответствии с методом (стратегией)."""
        if not data:
            data = f'logging function {traceback.extract_stack()[-2][2]}'
        text = f'log <==> {datetime.now()} <==> {data}'
        self.writer.write(text)


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
