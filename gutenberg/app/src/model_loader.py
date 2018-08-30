from abc import ABC, abstractmethod
from minio import Minio
from src.location import MinioLocation

import os


class BaseModelLoader(ABC):

    def __init__(self, location):
        self.location = location

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def unread(self):
        pass


class MinioLoader(BaseModelLoader):

    def __init__(self, location):
        BaseModelLoader.__init__(self, location)
        self.location = MinioLocation(location)

    def read(self):
        """
        :param location:
        :param local: Where to save the remote model locally?
        :return:
        """
        # todo: put this inside model config
        client = Minio(self.location.get_host(), access_key='admin',
                       secret_key='password', secure=False)
        client.fget_object(bucket_name=self.location.get_bucket(),
                           object_name=self.location.get_object_name(),
                           file_path=os.path.dirname(
                               os.path.realpath(__file__))
                                     + os.path.sep + self.location.get_object_name())


    def unread(self):
        pass

