

class User:
    def __init__(self, params: dict):
        self.name = None
        self.category = None
        for k, v in params.items():
            self.__setattr__(k, v)

    def __str__(self):
        return f'{self.name} - {self.category}'


class UserBuilder:
    def __init__(self):
        self.params = {}

    @property
    def personal_info(self):
        return PersonalInfoBuilder(self)

    @property
    def special_info(self):
        return SpecialInfoBuilder(self)

    def build(self):
        user = User(self.params)
        return user


class PersonalInfoBuilder:
    """Личная общая для всех информация."""

    def __init__(self, parent_builder):
        self.parent_builder = parent_builder

    def called(self, name):
        self.parent_builder.params['name'] = name
        return self

    def addressed(self, email):
        self.parent_builder.params['email'] = email
        return self.parent_builder



class SpecialInfoBuilder:
    """Специфичная для каждой категории пользователей."""
    def __init__(self, parent_builder):
        self.parent_builder = parent_builder

    def typed(self, category):
        self.parent_builder.params['category'] = category
        return self.parent_builder


class Student(User):
    count = -1

    def __init__(self, params: dict):
        super().__init__(params)
        self.__class__.count += 1
        self.id = self.count
        self.studied_courses = []

    def add_studied_courses(self, studied_courses:list):
        self.studied_courses.extend(studied_courses)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.category}'


class StudentBuilder(UserBuilder):
    def build(self):
        student = Student(self.params)
        return student

class Teacher(User):
    count = -1

    def __init__(self, params: dict):
        super().__init__(params)
        self.__class__.count += 1
        self.id = self.count
        self.taught_courses = []

    def add_taught_courses(self, taught_courses:list):
        self.taught_courses.extend(taught_courses)

    def __str__(self):
        return f'{self.id} - {self.name} - {self.category}'

class TeacherBuilder(UserBuilder):
    def build(self):
        teacher = Teacher(self.params)
        return teacher

class UserFactory:
    categories = {
        'teacher': TeacherBuilder,
        'student': StudentBuilder
    }

    @classmethod
    def create_user(cls, category):
        return cls.categories[category]()


if __name__ == '__main__':
    user1 = UserFactory.create_user('student'). \
        personal_info. \
        called('Bob'). \
        addressed('ww@ww.com'). \
        special_info. \
        typed('student'). \
        build()

    user2 = UserFactory.create_user('teacher'). \
                personal_info. \
                    called('John'). \
                    addressed('zz@ww.com'). \
                special_info. \
                    typed('teacher'). \
                build()

    user3 = UserFactory.create_user('teacher'). \
                personal_info. \
                    called('Sam'). \
                    addressed('aa@ww.com'). \
                special_info. \
                    typed('teacher'). \
                build()

    ub1 = UserFactory.create_user('teacher')
    ub2 = UserFactory.create_user('student')
    print(ub1)
    print(ub2)

    print(user1)
    print(user2)
    print(user3)
    print(user1 is user2)

    # 0 - Bob - ww@ww.com - student
    # 0 - John - zz@ww.com - student
    # False
    print(user1.__dict__)
    print(user2.__dict__)
