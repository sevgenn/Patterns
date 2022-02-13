"""Модуль, определяющий создание и поведение моделей курсов."""

import abc
from typing import List, Type
from collections.abc import Iterator, Iterable

from patterns.prototypes import PrototypeMixin


class ListIterator(Iterator):
    cursor: int = 0

    def __init__(self, collection: Type[List]):
        self._collection = collection

    def __next__(self):
        try:
            value = self._collection[self.cursor]
            self.cursor += 1
        except IndexError:
            raise StopIteration()
        return value


class Component(abc.ABC):
    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @abc.abstractmethod
    def is_composite(self):
        pass

    @abc.abstractmethod
    def add_to_parent(self):
        if self.parent:
            self.parent.children.append(self)

    def add_children(self, component):
        pass

    def remove_children(self, component):
        pass


class Composite(Component):
    def __init__(self, name, parent: Component=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.add_to_parent()

    def add_to_parent(self):
        if self.parent:
            self.parent.children.append(self)

    def add_children(self, component: Component):
        self.children.append(component)
        component.parent = self

    def remove_children(self, component: Component):
        self.children.remove(component)
        component.parent = None

    def is_composite(self) -> bool:
        return True

    def count_children(self):
        quantity = len([item for item in self.children if not item.is_composite()])
        for item in self.children:
            if item.is_composite():
                quantity += item.count_children()
        return quantity


class Category(Composite, Iterable):
    count = -1

    def __init__(self, name, parent: Component=None):
        super().__init__(name, parent)
        self.__class__.count += 1
        self.id = self.count
        self.parent = parent
        self._courses = []

    def update_courses(self) -> None:
        """Обновляет список курсов в данной категории."""
        self.courses_list = [item for  item in self.children if not item.is_composite()]
        self._courses = self.courses_list

    def __iter__(self) -> ListIterator:
        return ListIterator(self._courses)


class Course(PrototypeMixin, Component, Iterable):
    count = -1

    def __init__(self, name: str, parent: Component):
        self.__class__.count += 1
        self.id = self.count
        self.name = name
        self.parent = parent
        self.add_to_parent()
        self.teachers = []
        self.students = []

    def is_composite(self):
        return False

    def add_to_parent(self):
        self.parent.children.append(self)
        self.parent.update_courses()

    def __iter__(self) -> ListIterator:
        return ListIterator(self.students)

    def __str__(self):
        return f'Course {self.name}'


class CategoryFactory:

    @classmethod
    def create_category(cls, name: str, parent: Category=None):
        category = Category(name, parent)
        return category


class OnlineCourse(Course):
    pass


class OfflineCourse(Course):
    pass


class CourseFactory:
    types = {
        'online': OnlineCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create_course(cls, type_, name, parent: Category):
        return cls.types[type_](name, parent)


if __name__ == '__main__':
    category1 = CategoryFactory.create_category('programming')
    category2 = CategoryFactory.create_category('web', category1)
    category3 = CategoryFactory.create_category('python', category2)

    course1 = CourseFactory.create_course('online', 'django', category3)
    print(type(course1))
    print(course1)

    course2 = CourseFactory.create_course('offline', 'flask', category3)
    print(course2)

    print(category3._courses)
    for i in category3:
        print(i)
