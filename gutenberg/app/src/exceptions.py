
class InvalidDataError(Exception):

    def __init__(self, message):
        self.message = message


class InvalidType(Exception):

    def __init__(self, message):
        self.message = message
