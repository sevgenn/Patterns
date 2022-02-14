import threading
import sqlite3

from users_models import User
from courses_models import Category, Course
from site_models import Site

from courses_models import ListIterator, Component, Composite
from collections.abc import Iterator, Iterable
from patterns.prototypes import PrototypeMixin


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


#################################################################################
class Student(User, DomainObject):
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

########################################################################


class Mapper:
    tables = {
        'students': Student,
        'categories': Category,
        'courses': Course
    }

    def __init__(self, connection, tablename):
        self.connection = connection
        self.cursor = connection.cursor
        self.table = tablename

    def find_by_id(self, id):
        statement = f'SELECT * FROM {self.table} WHERE id=?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return self.tables[self.table](*result)
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
        statement  = f'UPDATE {self.table} SET name=? WHERE id=?'
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
            return Mapper(connection, tablename='students')
        if isinstance(obj, Category):
            return Mapper(connection, tablename='categories')
        if isinstance(obj, Course):
            return Mapper(connection, tablename='courses')


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert()
        self.update()
        self.remove()

    def insert(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def remove(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).remove(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


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


if __name__ == '__main__':
    connection = sqlite3.connect('patterns.db')
    site = Site()
    try:
            UnitOfWork.new_current()
            new_cat1 = site.create_course_category('programming')
            print('new_cat1: ', new_cat1)
            print(new_cat1.__dir__())
            new_cat1.mark_new()
            new_cat2 = site.create_course_category('web', new_cat1)
            new_cat2.mark_new()
            new_cat3 = site.create_course_category('python', new_cat2)
            new_cat1.mark_new()

            category_mapper = Mapper(connection, 'categories')
            UnitOfWork.get_current().commit()

    except Exception as e:
        print('Error: ', e.args)
    finally:
        UnitOfWork.get_current()

    print(UnitOfWork.get_current())

    try:
            new_course1 = site.create_course('online', 'django', new_cat3)
            new_course1.mark_new()
            new_course2 = site.create_course('online', 'flask', new_cat3)
            new_course2.mark_new()
            new_course3 = site.create_course('online', 'php', new_cat2)
            new_course3.mark_new()

            course_mapper = Mapper(connection, 'courses')
            UnitOfWork.get_current().commit()

    except Exception as e:
        print('Error: ', e.args)
    finally:
        UnitOfWork.get_current()

    print(UnitOfWork.get_current())

    try:
            new_student1 = site.create_user('student', 'Sam')
            new_student1.mark_new()
            new_student2 = site.create_user('student', 'Bob')
            new_student2.mark_new()
            new_student3 = site.create_user('student', 'Pit')
            new_student3.mark_new()

            student_mapper = Mapper(connection, 'students')
            UnitOfWork.get_current().commit()

    except Exception as e:
        print('Error: ', e.args)
    finally:
        UnitOfWork.get_current()

    print(UnitOfWork.get_current())
