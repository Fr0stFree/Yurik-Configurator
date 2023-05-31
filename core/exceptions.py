class ValidationError(Exception):
    pass


class InvalidValueError(ValidationError):
    pass


class UnknownSensorTypeError(ValidationError):
    pass


class UnknownSignalTypeError(ValidationError):
    pass
