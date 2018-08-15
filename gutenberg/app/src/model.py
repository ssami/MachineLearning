import time
from src.generator import ModelHashGenerator
from src.exceptions import InvalidDataError


class ModelInfo():

    def __init__(self, description, metrics, location,
                 hash_generator=ModelHashGenerator()):
        self.__required_checks(
            hash_generator=hash_generator,
            location=location
        )
        self.hash = hash_generator.generate()
        self.timestamp = time.time()
        self.description = description
        self.metrics = metrics
        self.location = location

    def __required_checks(self, **kwargs):
        for k,v in kwargs.items():
            if v is None:
                raise InvalidDataError('{0} cannot be empty'.format(k))

    @property
    def items(self):
        return self.__dict__