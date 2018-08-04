from abc import ABC, abstractmethod
import time


class HashGenerator(ABC):

    @abstractmethod
    def generate(self):
        pass


class ModelHashGenerator(HashGenerator):

    def generate(self):

        return int(time.time())