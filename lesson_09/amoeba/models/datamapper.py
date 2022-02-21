import sqlite3

from models.users_models import Student
from models.courses_models import Category, Course
from settings import settings
from models.site_models import Site
from patterns.domain import UnitOfWork


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
        statement = f'INSERT INTO {self.table} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
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

connection = sqlite3.connect(settings['DB'])

class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)
        if isinstance(obj, Course):
            return CourseMapper(connection)
        else:
            print('FATAL')


if __name__ == '__main__':
    pass
    # connection = sqlite3.connect('patterns.db')
    # site = Site()
    # UnitOfWork.new_current()
    # UnitOfWork.get_current().set_mapper_registry(MapperRegistry)
    # try:
    #     new_cat1 = site.create_course_category('programming')
    #     new_cat1.mark_new()
    #     new_cat2 = site.create_course_category('web', new_cat1)
    #     new_cat2.mark_new()
    #     new_cat3 = site.create_course_category('python', new_cat2)
    #     new_cat1.mark_new()
    #
    #     new_course1 = site.create_course('online', 'django', new_cat3)
    #     new_course1.mark_new()
    #     new_course2 = site.create_course('online', 'flask', new_cat3)
    #     new_course2.mark_new()
    #     new_course3 = site.create_course('online', 'php', new_cat2)
    #     new_course3.mark_new()
    #
    #     new_student1 = site.create_user('student', 'Sam')
    #     new_student1.mark_new()
    #     new_student2 = site.create_user('student', 'Bob')
    #     new_student2.mark_new()
    #     new_student3 = site.create_user('student', 'Pit')
    #     new_student3.mark_new()
    #
    #     UnitOfWork.get_current().commit()
    #
    #
    # except Exception as err:
    #     print('Error: ', err.args)
    # finally:
    #     UnitOfWork.get_current()
    #
    # print(UnitOfWork.get_current())
