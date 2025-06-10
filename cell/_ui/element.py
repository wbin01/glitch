#/usr/bin/env python3
from PySide6 import QtQuick


class Element(object):
    """..."""
    def __init__(
            self, qt_quick_item: QtQuick.QQuickItem, *args, **kwargs) -> None:
        """..."""
        self.__obj = qt_quick_item
        self.object_id = '_' + str(id(self))

    @property
    def object_id(self) -> str:
        """..."""
        return self._obj.property('id')

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self._obj.setProperty('id', object_id)
        self._obj.setProperty('objectName', object_id)

    @property
    def _obj(self) -> str:
        """..."""
        return self.__obj

    @_obj.setter
    def _obj(self, obj: str) -> None:
        self.__obj = obj
