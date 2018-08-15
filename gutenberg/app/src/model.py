import time
from src.generator import ModelHashGenerator


class ModelInfo():

    def __init__(self, description, metrics, location, hash_generator=ModelHashGenerator()):
        self.hash = hash_generator.generate()
        self.timestamp = time.time()
        self.description = description
        self.metrics = metrics
        self.location = location

    @property
    def items(self):
        return self.__dict__