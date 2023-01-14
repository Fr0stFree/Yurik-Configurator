class ConfiguratorError(Exception):
    pass


class InvalidValueError(ConfiguratorError):
    pass


class UnknownSensorTypeError(ConfiguratorError):
    pass