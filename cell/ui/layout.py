#/usr/bin/env python3


class Layout(object):
    """..."""
    pass


class Element(object):
    """..."""
    pass


class Layout(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__id = '_' + str(id(self))
        self.__qml = self.__id
        self.__added_objects = []

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__qml = self.__qml.replace(
            f'id: {self.__id}', f'id: {object_id}').replace(
            f'objectName: "{self.__id}"', f'objectName: "{object_id}"')
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

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
        setattr(self, obj.object_id, obj)
        return obj
