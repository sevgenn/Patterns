"""Модуль, определяющий создание и поведение моделей курсов."""

from patterns.prototypes import PrototypeMixin


class Course(PrototypeMixin):
    def __init__(self, name: str, category: str):
        self.name = name
        self.category = category
        self.print_content = {}
        self.video_content = []
        self.teachers = []
        self.students = []

    def __str__(self):
        return f'Course {self.name}'


class CourseCategory(PrototypeMixin):
    def __init__(self, name: str, sub_category: str):
        self.name = name
        self.sub_categories = []
        self.courses = []
        self.add_sub_category(sub_category)

    def add_sub_category(self, sub_category):
        self.sub_categories.append(sub_category)

    def count_courses(self):
        quantity = len(self.courses)
        if self.sub_categories:
            for item in self.sub_categories:
                quantity += len(item.count_courses())
        return quantity


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
    def create_course(cls, type_, name, category):
        return cls.types[type_](name, category)


if __name__ == '__main__':
    course1 = CourseFactory.create_course('online', 'Python', 'programming')
    print(type(course1))
    print(course1)

    course2 = CourseFactory.create_course('offline', 'Java', 'programming')
    print(course2)
