from pypattyrn.behavioral.null import Null


class NoLog(Null):
    """
    A class that represents a no-operation logger.

    This class is used to provide a logger interface that does nothing.
    It can be used as a placeholder or default logger to avoid null checks.

    Methods:
        __init__(): Initializes the NoLog instance.
    """
    def __init__(self):
        """
        Initialize the NoLog instance.
        """
        super(NoLog, self).__init__()
