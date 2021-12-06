class QueryError(Exception):
    def __init__(self, msg):
        super().__init__(msg)

class EmptyQueryError(Exception):
    def __init__(self):
        super().__init__("Please provide some parameters to make a query.")