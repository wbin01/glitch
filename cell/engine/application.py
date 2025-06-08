#/usr/bin/env python3
from .handler import Handler


class Application(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__handler = None
        # ...

    @property
    def handler(self) -> None:
        """..."""
        return self.__handler

    @handler.setter
    def handler(self, handler: Handler) -> None:
        self.__handler = handler

    def exec(self):
        """..."""
        if self.__handler:
            print(self.__handler.qml_code())
