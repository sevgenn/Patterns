"""Модуль сохранения данных в json-файл."""

import os
import json
from amoeba.request import Request


class StorageManager:
    """Класс, обрабатывающий запись данных в файл и чтение."""

    @classmethod
    def create_storage_dir(cls, request: Request, file_name) -> str:
        """Возвращает путь до файла-хранилища."""
        storage_dir = os.path.join(request.settings.get('BASE_DIR'), request.settings.get('STORAGE_DIR'))
        return os.path.join(storage_dir, file_name)

    @classmethod
    def get_from_json(cls, request: Request, file_name) -> list:
        """Возвращает содержимое json-файла."""
        storage_path = cls.create_storage_dir(request, file_name)
        with open(storage_path, 'r') as file_read:
            return json.load(file_read)

    @classmethod
    def add_to_json(cls, request: Request, file_name, data: dict):
        """Добавляет данные в файл."""
        content = []
        storage_path = cls.create_storage_dir(request, file_name)
        if os.path.isfile(storage_path):
            data_json = cls.get_from_json(request, file_name)
            content.extend(data_json)
        content.append(data)
        with open(storage_path, 'w') as file_write:
            json.dump(content, file_write, ensure_ascii=False, indent=2, separators=(',', ': '))
            file_write.write('\n')
