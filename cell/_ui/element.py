#/usr/bin/env python3
from PySide6 import QtQuick, QtCore


class Element(object):
    """..."""
    def __init__(
            self, qt_quick_item: QtQuick.QQuickItem, *args, **kwargs) -> None:
        """
        self.qml is instance: static/elements/<element>.qml
        """
        self.__obj = qt_quick_item
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
    def _obj(self) -> str:
        """..."""
        return self.__obj

    @_obj.setter
    def _qml(self, obj: str) -> None:
        self.__obj = obj

    @property
    def _qml(self) -> str:
        """..."""
        return self.__qml

    @_qml.setter
    def _qml(self, qml: str) -> None:
        self.__qml = qml
