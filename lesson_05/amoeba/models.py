"""Модуль, определяющий создание и поведение моделей."""

from patterns.prototypes import PrototypeMixin

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def __str__(self):
        return f'{self.id} - {self.name}'

class Student(User):
    __slots__ = ('id', 'name', 'studied_courses')

    def __init__(self, id, name):
        super().__init__(id, name)
        self.studied_courses = []

    def add_studied_courses(self, studied_courses:list):
        self.studied_courses.extend(studied_courses)

class Teacher(User):
    __slots__ = ('id', 'name', 'taught_courses')

    def __init__(self, id, name):
        super().__init__(id, name)
        self.taught_courses = []

    def add_taught_courses(self, taught_courses:list):
        self.taught_courses.extend(taught_courses)

class StudentFactory:
    count = -1

    def create_student(self, name):
        self.count += 1
        return Student(self.count, name)

class TeacherFactory:
    count = -1

    def create_teacher(self, name):
        self.count += 1
        return Teacher(self.count, name)


class UserFactory:
    roles = {
        'teacher': TeacherFactory,
        'student': StudentFactory
    }

    @classmethod
    def create_user(cls, role):
        return cls.roles[role]()


class Course(PrototypeMixin):
    pass

class OnlineCourse(Course):
    pass

class OfflineCourse(Course):
    pass

class CourseBuilder:
    def __init__(self, course):
        self.course = course

    @property
    def content(self):
        return CourseContentBuilder(self.course)

    @property
    def teach(self):
        return CourseTeachersBuilder(self.course)

    def build(self):
        return self.course

class OnlineCourseBuilder(CourseBuilder):
    def __init__(self, course):
        super().__init__(course)
        self.course = course

    @property
    def url_address(self):
        return CourseUrlBuilder(self.course)

    # @property
    # def content(self):
    #     return CourseContentBuilder(self.course)
    #
    # @property
    # def teach(self):
    #     return CourseTeachersBuilder(self.course)
    #
    # def build(self):
    #     return self.course

class CourseUrlBuilder(OnlineCourseBuilder):
    def __init__(self, course):
        super().__init__(course)
        self.course = course

    def url_address(self, url):
        self.course.url_address = url
        return self

class CourseContentBuilder(CourseBuilder):
    def __init__(self, course):
        super().__init__(course)
        self.course = course



class CourseTeachersBuilder(CourseBuilder):
    def __init__(self, course):
        super().__init__(course)
        self.course = course

class CourseFactorie:
    types = {
        'online': 'OnlineCourse',
        'offline': 'OfflineCourse'
    }

    @classmethod
    def create_course(cls, type, name):
        return cls.types[type](name)



if __name__ == '__main__':
    uf1 = UserFactory.create_user('student')
    uf2 = UserFactory.create_user('teacher')

    s1 = uf1.create_student('bob')
    s2 = uf1.create_student('john')
    s3 = uf1.create_student('clark')
    s1.add_studied_courses(['Python', 'Java'])

    t1 = uf2.create_teacher('cindy')
    t2 = uf2.create_teacher('john')
    t1.add_taught_courses(['JS'])

    print(s1, s1.studied_courses)
    print(s2)
    print(s3)
    print(t1, t1.taught_courses)
    print(t2)

