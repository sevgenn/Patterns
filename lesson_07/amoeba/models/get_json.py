"""Определяет преобразование содержимого класса в строку json."""

from abc import ABC, abstractmethod
import json
from models.site_models import Site


class DataToJson(ABC):
    @abstractmethod
    def get_json(self):
        pass


class CoursesToJson(DataToJson):
    def __init__(self, site: Site):
        self.site = site

    def get_json(self):
        data = {}
        categories_list = self.site.get_categories()
        for category in categories_list:
            courses_list = [course.name for course in category]
            data.update({category.name: courses_list})

        return json.dumps(data, ensure_ascii=False, indent=4)
