import threading
import sqlite3

connection = sqlite3.connect('patterns.db')


class DomainObject:
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class UnitOfWork:
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def set_mapper_registry(self, mapper_registry):
        self.mapperregistry = mapper_registry

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
            self.mapperregistry.get_mapper(obj).insert(obj)

    def update(self):
        for obj in self.dirty_objects:
            self.mapperregistry.get_mapper(obj).update(obj)

    def remove(self):
        for obj in self.removed_objects:
            self.mapperregistry.get_mapper(obj).remove(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work
