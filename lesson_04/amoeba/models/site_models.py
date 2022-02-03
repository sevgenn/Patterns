"""Модуль, описывающий модель сайта."""

from models.users_models import UserFactory
from models.courses_models import CourseFactory

class Site:
    """Класс, описывающий сайт."""
    def __init__(self):
        self._courses = []
        self._teachers = []
        self._students = []

    def get_courses(self):
        """Возвращает список курсов."""
        return self._courses

    def create_course(self, category: str, name: str):
        """Добавляет курс в список."""
        course = CourseFactory.create_course(category, name)
        self._courses.append(course)

    def get_course(self, name):
        """Вщзвращает курс по названию."""
        for item in self._courses:
            if item.name == name:
                return item
        return None

    def create_user(self, category: str, name: str):
        """Добавляет ппользователя в список студентов или преподавателей."""
        user = UserFactory.create_user(category, name)

        if category == 'student':
            self._students.append(user)
        else:
            self._teachers.append(user)

    def get_teachers(self):
        """Возвращает список преподавателей."""
        return self._teachers

    def get_students(self):
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
