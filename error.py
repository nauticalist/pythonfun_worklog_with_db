class Error(Exception):
    """
    Base class for custom errors
    """
    pass


class ValueNotInRange(Error):
    """
    Raise when the input value is not in the list
    """
    pass
