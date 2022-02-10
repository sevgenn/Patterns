"""Модуль, определяющий создание и поведение моделей курсов."""

import abc
from patterns.prototypes import PrototypeMixin


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


class Course(PrototypeMixin, Component):
    def __init__(self, name: str):
        self.name = name
        self.teachers = []
        self.students = []

    def is_composite(self):
        return False

    def __str__(self):
        return f'Course {self.name}'


class Category(Composite):
    count = -1

    def __init__(self, name, parent: Component=None):
        super().__init__(name, parent)
        self.__class__.count += 1
        self.id = self.count

    @property
    def courses(self):
        """Возвращает список курсов в данной категории."""
        self.courses_list = [item for  item in self.children if not item.is_composite()]
        return self.courses_list


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
    def create_course(cls, type_, name):
        return cls.types[type_](name)


if __name__ == '__main__':
    course1 = CourseFactory.create_course('online', 'Python')
    print(type(course1))
    print(course1)

    course2 = CourseFactory.create_course('offline', 'Java')
    print(course2)
