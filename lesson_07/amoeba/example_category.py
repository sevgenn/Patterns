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
    pass


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


class Site:
    """Класс, описывающий сайт."""
    def __init__(self):
        self._courses = []
        self._course_categories = []
        self._teachers = []
        self._students = []

    def create_course(self, type: str, name: str, category: Category):
        """Добавляет курс в список."""
        new_course = CourseFactory.create_course(type, name)
        category.add_children(new_course)
        self._courses.append(new_course)
        return new_course

    def create_course_category(self, name: str, parent: Component=None):
        """Создает ровую категорию курсов."""
        new_category = CategoryFactory.create_category(name, parent)
        self._course_categories.append(new_category)
        return new_category

    def get_courses(self):
        """Возвращает список курсов."""
        return self._courses

    def get_course(self, name):
        """Вщзвращает курс по названию."""
        for item in self._courses:
            if item.name == name:
                return item
        return None

    def get_categories(self):
        """Возвращает список категорий курсов."""
        return self._course_categories


if __name__ == '__main__':
    site = Site()
    cat1 = site.create_course_category('programming')
    cat2 = site.create_course_category('web', cat1)
    cat3 = site.create_course_category('python', cat2)

    course1 = site.create_course('online', 'django', cat3)
    course2 = site.create_course('online', 'flask', cat3)
    course3 = site.create_course('online', 'php', cat2)

    cats = [item.name for item in site.get_categories()]
    print(cats)
    courses = [item.name for item in site.get_courses()]
    print(courses)
    print(cat2.__dict__)
    print(cat1.count_children())
