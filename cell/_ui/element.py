#/usr/bin/env python3


class Element(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """
        self.qml is instance: static/elements/<element>.qml
        """
        self.__id = '_' + str(id(self))
        self.__qml = self.__id

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
