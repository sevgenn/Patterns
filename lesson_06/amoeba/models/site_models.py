"""Модуль, описывающий модель сайта."""

from typing import Type, List
from models.users_models import Teacher, Student, UserFactory
from models.courses_models import Component, Course, Category, CourseFactory, CategoryFactory

class Site:
    """Класс, описывающий сайт."""
    def __init__(self):
        self._courses = []
        self._course_categories = []
        self._teachers = []
        self._students = []

    def add_course(self, course: Course):
        """Добавляет новый курс."""
        self._courses.append(course)

    def create_course(self, type: str, name: str, category: Category):
        """Добавляет курс в список."""
        new_course = CourseFactory.create_course(type, name, category)
        self.add_course(new_course)
        return new_course

    def create_course_category(self, name: str, parent: Component=None):
        """Создает новую категорию курсов."""
        new_category = CategoryFactory.create_category(name, parent)
        self._course_categories.append(new_category)
        return new_category

    def create_user(self, category: str, name: str):
        """Добавляет ппользователя в список студентов или преподавателей."""
        new_user = UserFactory.create_user(category, name)
        if category == 'student':
            self._students.append(new_user)
        else:
            self._teachers.append(new_user)

    def get_courses(self) -> List[Type[Course]]:
        """Возвращает список курсов."""
        return self._courses

    def get_course_by_name(self, name) -> Type[Course]:
        """Вщзвращает курс по названию."""
        for item in self._courses:
            if item.name == name:
                return item
        return None

    def get_course_by_id(self, id) -> Type[Course]:
        """Вщзвращает курс по ID."""
        for item in self._courses:
            if item.id == id:
                return item
        return None

    def get_categories(self) -> List[Type[Category]]:
        """Возвращает список категорий курсов."""
        return self._course_categories

    def get_category_by_id(self, id: str) -> Type[Category]:
        """Возвращает категорию по id."""
        for item in self._course_categories:
            if item.id == id:
                return item
            else:
                return None

    def get_category_by_name(self, name: str) -> Type[Category]:
        """Возвращает категорию по имени."""
        for item in self._course_categories:
            if item.name == name:
                return item
            else:
                return None

    def get_teachers(self) -> List[Type[Teacher]]:
        """Возвращает список преподавателей."""
        return self._teachers

    def get_students(self) -> List[Type[Student]]:
        """Возвращает список преподавателей."""
        return self._students

    def get_student_by_name(self, name: str) -> Type[Student]:
        """Возвращает объект студента по имени."""
        for item in self._students:
            if item.name == name:
                return item
            else:
                return None


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
    print('<Quantity>:', cat1.count_children())

    print('<All courses>:', site.get_courses())
    print('<One course>:', site.get_courses()[1])


    site.create_user('student', 'Bob')
    print(site.get_students()[0].name)
    print(site.get_students()[0].__dict__)
