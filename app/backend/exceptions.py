class ValidationError(Exception):
    pass


class InvalidFieldError(Exception):
    def __init__(self, message: str, name: str, column: str) -> None:
        super().__init__(message)
        self.name = name
        self.column = column


class InvalidSkipFlag(Exception):
    pass
