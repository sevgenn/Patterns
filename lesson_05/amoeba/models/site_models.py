"""Модуль, описывающий модель сайта."""

from typing import Type, List
from models.users_models import Teacher, Student, UserFactory
from models.courses_models import Course, CourseFactory, CourseCategory

class Site:
    """Класс, описывающий сайт."""
    def __init__(self):
        self._courses = []
        self._course_categories = []
        self._teachers = []
        self._students = []

    def create_course(self, type: str, name: str, category: str):
        """Добавляет курс в список."""
        new_course = CourseFactory.create_course(type, name, category)
        self._courses.append(new_course)

    def create_course_category(self, name: str, category: str = ''):
        """Создает ровую категорию курсов."""
        new_category = CourseCategory(name, category)
        self._course_categories.append(new_category)

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

    def get_course(self, name) -> Type[Course]:
        """Вщзвращает курс по названию."""
        for item in self._courses:
            if item.name == name:
                return item
        return None

    def get_categories(self) -> List[Type[CourseCategory]]:
        """Возвращает список категорий курсов."""
        return self._course_categories

    def get_teachers(self) -> List[Type[Teacher]]:
        """Возвращает список преподавателей."""
        return self._teachers

    def get_students(self) -> List[Type[Student]]:
        """Возвращает список преподавателей."""
        return self._students


if __name__ == '__main__':
    site = Site()

    site.create_course('online', 'rt')
    print(site.get_courses()[0])
    print(site.get_course('rt'))

    site.create_user('student', 'Bob')
    print(site.get_students()[0].name)
    print(site.get_students()[0].__dict__)
