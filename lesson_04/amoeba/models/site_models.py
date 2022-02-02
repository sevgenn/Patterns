"""Модуль, описывающий модель сайта."""

class Site:
    """Класс, описывающий сайт."""
    def __init__(self):
        self._courses = []
        self._teachers = []
        self._students = []

    def get_courses(self):
        """Возвращает список курсов."""
        return self._courses

    def add_course(self, course):
        """Добавляет курс в список."""
        self._courses.append(course)

    def get_course(self, name):
        """Вщзвращает курс по названию."""
        for item in self._courses:
            if item.name == name:
                return item
        return None

    def get_teachers(self):
        """Возвращает список преподавателей."""
        return self._teachers

    def add_teacher(self, teacher):
        """Добавляет преподавателя в список."""
        self._teachers.append(teacher)

    def get_students(self):
        """Возвращает список преподавателей."""
        return self._students

    def add_student(self, student):
        """Добавляет преподавателя в список."""
        self._students.append(student)


if __name__ == '__main__':
    site = Site()


    site.add_courses('rt')
    print(site.get_courses())
