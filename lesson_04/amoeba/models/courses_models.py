"""Модуль, определяющий создание и поведение моделей курсов."""

from patterns.prototypes import PrototypeMixin


class Course(PrototypeMixin):
    pass


class OnlineCourse(Course):
    def __init__(self, name: str):
        self.name = name
        self.category = 'online'
        self.print_content = {}
        self.video_content = []
        self.teachers = []
        self.url_address = ''

    def __str__(self):
        return f'Course {self.name}'


class OfflineCourse(Course):
    def __init__(self, name: str):
        self.name = name
        self.category = 'offline'
        self.print_content = {}
        self.teachers = []
        self.address = ''

    def __str__(self):
        return f'Course {self.name}'


class CourseFactory:
    categories = {
        'online': OnlineCourse,
        'offline': OfflineCourse
    }

    @classmethod
    def create_course(cls, category, name):
        return cls.categories[category](name)


if __name__ == '__main__':
    course1 = CourseFactory.create_course('online', 'Python')
    print(type(course1))
    print(course1)

    course2 = CourseFactory.create_course('offline', 'Java')
    print(course2)
