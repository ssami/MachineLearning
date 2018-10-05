from abc import ABC, abstractmethod

##
# Couchbase:
# username: admin
# password: password
##
from couchbase.bucket import Bucket
from couchbase.views.iterator import View

class ModelInfoDatabase(ABC):

    def __init__(self, host, port, user=None, password=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = self.__create__()

    @abstractmethod
    def __create__(self):
        pass

    @abstractmethod
    def find_model_info(self, key):
        pass


    @abstractmethod
    def find_all_model_info(self, limit=10):
        pass


    @abstractmethod
    def store_model_info(self, key, model_info):
        pass


class FeedbackDatabase(ABC):
    """
    Two options for feedback:
    1. create multiple feedback buckets, which needs us to do Couchbase API calls
    2. create a single bucket but have each key store giant documents
    For now, I decided to go with option 2) for simplicity.
    Ideally when we create a new object to store model_info we should also
    create a new bucket for feedback!
    """

    CONNSTR = 'couchbase://localhost:8091/feedback'

    @abstractmethod
    def store_feedback(self, key, feedback_info):
        pass

    @abstractmethod
    def get_feedback(self, key):
        pass


class CouchModelInfo(ModelInfoDatabase) :

    CONNSTR = 'couchbase://localhost:8091/model_info'
    DDOC = 'dev_metrics'
    VIEW = 'model_metrics'


    def __create__(self):
        return Bucket(self.CONNSTR, self.user, self.password)

    def find_model_info(self, key):
        return self.db.get(key)

    def store_model_info(self, key, model_info):
        self.db.insert(key, model_info)

    def find_all_model_info(self, limit=10):
        view = View(self.db, self.DDOC, self.VIEW)
        results = []
        count = 0
        for v in view:
            if count > limit:
                break
            results.append((v.docid, v.key, v.value))
            count += 1

        return results


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
