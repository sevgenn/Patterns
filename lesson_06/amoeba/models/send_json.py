"""Определяет преобразование содержимого класса в строку json."""

from abc import ABC, abstractmethod
import json
from models.site_models import Site


class DataToJson(ABC):
    @abstractmethod
    def send_json(self):
        pass


class CoursesToJson(DataToJson):
    def __init__(self, site: Site):
        self.site = site

    def send_json(self):
        data = {}
        categories_list = self.site.get_categories()
        for category in categories_list:
            courses_list = [item.name for item in category.courses]
            data.update({category.name: courses_list})
        return json.dumps(data, ensure_ascii=False, indent=4)
