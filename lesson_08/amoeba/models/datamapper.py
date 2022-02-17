import sqlite3
import abc
from typing import List, Type
from mapper import UnitOfWork
from collections.abc import Iterator, Iterable

from patterns.prototypes import PrototypeMixin
from mapper import DomainObject

#############################  CATEGORIES-COURSES MODELS  #########################################

class ListIterator(Iterator):
    cursor: int = 0

    def __init__(self, collection: Type[List]):
        self._collection = collection

    def __next__(self):
        try:
            value = self._collection[self.cursor]
            self.cursor += 1
        except IndexError:
            raise StopIteration()
        return value


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

    @abc.abstractmethod
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


class Category(Composite, Iterable, DomainObject):
    count = -1

    def __init__(self, name, parent: Component=None):
        super().__init__(name, parent)
        self.__class__.count += 1
        self.id = self.count
        self.parent = parent
        self._courses = []

    def update_courses(self) -> None:
        """Обновляет список курсов в данной категории."""
        self.courses_list = [item for  item in self.children if not item.is_composite()]
        self._courses = self.courses_list

    def __iter__(self) -> ListIterator:
        return ListIterator(self._courses)


class Course(PrototypeMixin, Component, Iterable, DomainObject):
    count = -1

    def __init__(self, name: str, parent: Component):
        self.__class__.count += 1
        self.id = self.count
        self.name = name
        self.parent = parent
        self.add_to_parent()
        self.teachers = []
        self.students = []

    def is_composite(self):
        return False

    def add_to_parent(self):
        self.parent.children.append(self)
        self.parent.update_courses()

    def __iter__(self) -> ListIterator:
        return ListIterator(self.students)

    def __str__(self):
        return f'Course {self.name}'


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
    def create_course(cls, type_, name, parent: Category):
        return cls.types[type_](name, parent)

#############################  USER MODELS  #########################################


class User(DomainObject):
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

    def called(self, name: str):
        self.parent_builder.params['name'] = name
        return self

    def addressed(self, email: str=''):
        self.parent_builder.params['email'] = email
        return self.parent_builder



class SpecialInfoBuilder:
    """Специфичная для каждой категории пользователей."""
    def __init__(self, parent_builder):
        self.parent_builder = parent_builder

    def typed(self, category: str):
        self.parent_builder.params['category'] = category
        return self.parent_builder


class Student(User):
    count = -1

    def __init__(self, params: dict):
        super().__init__(params)
        self.__class__.count += 1
        self.id = self.count
        self._studied_courses = []

    @property
    def studied_courses(self):
        return self._studied_courses

    def add_studied_courses(self, course):
        self._studied_courses.append(course)

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
    def create_user(cls, category: str, name: str, email: str=''):
        user = cls.categories[category](). \
                personal_info. \
                    called(name). \
                    addressed(email). \
                special_info. \
                    typed(category). \
                build()
        return user

#############################  SITE MODELS  #########################################


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
        return new_user

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


####################  DATAMAPPER  #####################################

class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found exception: {message}')


class DbInsertException(Exception):
    def __init__(self, message):
        super().__init__(f'DB insert error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'DB update error: {message}')


class DbRemoveException(Exception):
    def __init__(self, message):
        super().__init__(f'DB remove error: {message}')


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = 'students'

    def find_by_id(self, id):
        statement = f'SELECT * FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'Record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table} (id, name) VALUES (?, ?)'
        self.cursor.execute(statement, (obj.id, obj.name))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbInsertException(err.args)

    def update(self, obj):
        statement = f'UPDATE {self.table} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def remove(self, obj):
        statement = f'DELETE FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbRemoveException(err.args)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = 'categories'

    def find_by_id(self, id):
        statement = f'SELECT * FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'Record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table} (name, parent_id) VALUES (?, ?)'
        parent_name = obj.parent.name if obj.parent else None
        self.cursor.execute(statement, (obj.name, parent_name))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbInsertException(err.args)

    def update(self, obj):
        statement = f'UPDATE {self.table} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def remove(self, obj):
        statement = f'DELETE FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbRemoveException(err.args)


class CourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table = 'courses'

    def find_by_id(self, id):
        statement = f'SELECT * FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'Record with id={id} not found')

    def insert(self, obj):
        statement = f'INSERT INTO {self.table} (name, category_id) VALUES (?, ?)'
        self.cursor.execute(statement, (obj.name, obj.parent.name))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbInsertException(err.args)

    def update(self, obj):
        statement = f'UPDATE {self.table} SET name=? WHERE id=?'
        self.cursor.execute(statement, (obj.name, obj.id))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbUpdateException(err.args)

    def remove(self, obj):
        statement = f'DELETE FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as err:
            raise DbRemoveException(err.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if (obj.__class__ == Category):
            return CategoryMapper(connection)
        if isinstance(obj, Course):
            return CourseMapper(connection)
        else:
            print('FATAL')


if __name__ == '__main__':
    connection = sqlite3.connect('patterns.db')
    site = Site()
    UnitOfWork.new_current()
    UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
    try:
        new_cat1 = site.create_course_category('programming')
        new_cat1.mark_new()
        new_cat2 = site.create_course_category('web', new_cat1)
        new_cat2.mark_new()
        new_cat3 = site.create_course_category('python', new_cat2)
        new_cat1.mark_new()

        new_course1 = site.create_course('online', 'django', new_cat3)
        new_course1.mark_new()
        new_course2 = site.create_course('online', 'flask', new_cat3)
        new_course2.mark_new()
        new_course3 = site.create_course('online', 'php', new_cat2)
        new_course3.mark_new()

        new_student1 = site.create_user('student', 'Sam')
        new_student1.mark_new()
        new_student2 = site.create_user('student', 'Bob')
        new_student2.mark_new()
        new_student3 = site.create_user('student', 'Pit')
        new_student3.mark_new()

        UnitOfWork.get_current().commit()


    except Exception as err:
        print('Error: ', err.args)
    finally:
        UnitOfWork.get_current()

    print(UnitOfWork.get_current())


"""
Если не передавать id студента:
Error:  ('Incorrect number of bindings supplied. The current statement uses 1, and there are 3 supplied.',)
"""
