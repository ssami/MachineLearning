import time
from src.generator import ModelHashGenerator


class ModelInfo():

    def __init__(self, description, metrics, hash_generator=ModelHashGenerator()):
        self.hash = hash_generator.generate()
        self.timestamp = time.time()
        self.description = description
        self.metrics = metrics

    def items(self):
        return {
            'hash': self.hash,
            'timestamp': self.timestamp,
            'description': self.description,
            'metrics': self.metrics
        }