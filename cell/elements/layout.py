#/usr/bin/env python3


class Layout(object):
    """..."""
    pass

class Element(object):
    """..."""
    pass

class Layout(Layout):
    """..."""
    def __init__(self, object_id: str, *args, **kwargs) -> None:
        """..."""
        self.__object_id = object_id
        self.__object_code = None
        self.__added_objects = []

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

    @property
    def added_objects(self) -> list:
        """..."""
        return self.__added_objects

    @added_objects.setter
    def added_objects(self, added_objects: list) -> None:
        self.__added_objects = added_objects

    def add(self, obj) -> Layout | Element:
        """..."""
        self.__added_objects.append(obj)
        return obj
