#/usr/bin/env python3


class Element(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__id = str(id(self))
        self.__qml = self.__id

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__qml = self.__qml.replace(f'id: {self.__id}', f'id: {object_id}')
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml
