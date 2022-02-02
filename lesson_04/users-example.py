"""Хотел сделать подобную реализацию для большей гибкости.
Почему не работает id, это понятно, в остальном все работает.
Но если наследую от UserBuilder конкретные классы StudentBuilder и TeacherBuilder,
все сыплется, текучесть интерфейса не поддерживается. Последующие вызываемые свойства
билдера воспринимаются как функция.
В чем причина, так и не понял. Возможно, я наследование в классах не очень понимаю.
Поэтому сделал реализацию, как на лекции.
"""

class User:
    def __init__(self):
        self.id = None
        self.name = None
        self.email = None
        self.category = None

    def __str__(self):
        return f'{self.id} - {self.name} - {self.email} - {self.category}'


class UserBuilder:
    def __init__(self, user):
        self.user = user

    @property
    def personal_info(self):
        return PersonalInfoBuilder(self.user)

    @property
    def special_info(self):
        return SpecialInfoBuilder(self.user)

    def build(self):
        return self.user


class PersonalInfoBuilder(UserBuilder):
    """Личная общая для всех информация."""
    count = -1

    def __init__(self, user):
        super().__init__(user)

    def id(self):
        self.count += 1
        self.user.id = self.count
        return self

    def called(self, name):
        self.user.name = name
        return self

    def addressed(self, email):
        self.user.email = email
        return self


class SpecialInfoBuilder(UserBuilder):
    """Специфичная для каждой категории пользователей."""
    def __init__(self, user):
        super().__init__(user)

    def typed(self, category):
        self.user.category = category
        return self


if __name__ == '__main__':
    user_builder1 = UserBuilder(User())
    user1 = user_builder1. \
                personal_info. \
                    id(). \
                    called('Bob'). \
                    addressed('ww@ww.com'). \
                special_info. \
                    typed('student'). \
                build()

    user_builder2 = UserBuilder(User())
    user2 = user_builder2. \
                personal_info. \
                    id(). \
                    called('John'). \
                    addressed('zz@ww.com'). \
                special_info. \
                    typed('student'). \
                build()

    print(user1)
    print(user2)
    print(user1 is user2)
    # 0 - Bob - ww@ww.com - student
    # 0 - John - zz@ww.com - student
    # False
