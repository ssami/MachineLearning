from abc import ABC, abstractmethod
import redis
from src.exceptions import InvalidType
from flask import g


class Database(ABC):

    def __init__(self, host, port, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = self.__create__()

    def get_db(self):
        return self.db

    @abstractmethod
    def __create__(self):
        pass

    @abstractmethod
    def store(self, key, info):
        pass

    @abstractmethod
    def find(self, key):
        pass


class RedisDB(Database):

    def __create__(self):
        return redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password
        )

    def store(self, key, info):
        """
        Clearly these are not the only two
        available params. The remainder are
        left as an exercise for the reader.
        :param key:
        :param info:
        :return:
        """
        if type(info) == dict:
            self.db.hmset(key, info)
        else:
            self.db.sadd(key, info)

    def find(self, key):
        return self.db.smembers(key)


def get_db(db_class, host='localhost', port='6379', user=None, password=None):
    # if 'db' not in g:
    #     g.db = redis.Redis(
    #         host="localhost",
    #         port=6379,
    #         password=None
    #     )
    # return g.db
    # TODO: make sure DB connection is created and cached
    for clz in Database.__subclasses__():
        if clz.__name__ == db_class:
            return clz(host, port, user, password)

    raise InvalidType('{0} is not a valid database type'.format(db_class))


def close_db():
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db)