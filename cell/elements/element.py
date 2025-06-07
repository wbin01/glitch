#/usr/bin/env python3


class Element(object):
    """..."""
    def __init__(self, object_id: str, *args, **kwargs) -> None:
        """..."""
        self.__object_id = object_id
        self.__object_code = None

    @property
    def object_id(self) -> str:
        """..."""
        return self.__object_id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__object_id = object_id

    @property
    def object_code(self) -> str:
        """..."""
        return self.__object_code

    @object_code.setter
    def object_code(self, object_code: str) -> None:
        self.__object_code = object_code
