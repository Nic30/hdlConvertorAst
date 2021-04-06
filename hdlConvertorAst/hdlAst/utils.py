

class CodePosition(object):
    __slots__ = [
        "start_line",
        "start_column",
        "stop_line",
        "stop_column",
    ]

    def __init__(self):
        self.start_line = None
        self.start_column = None
        self.stop_line = None
        self.stop_column = None

    def __repr__(self):
        return "<%s %r:%r to %r:%r>" % (self.__class__.__name__,
                                        self.start_line, self.start_column,
                                        self.stop_line, self.stop_column)
