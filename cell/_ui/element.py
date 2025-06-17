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
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        Get:
            (5, 10, 5, 10)

        Set:
            Missing value, only from left to right.

            self.my_button.margins = 5
            self.my_button.margins = 5, 10
            self.my_button.margins = 5, 10, 5
            self.my_button.margins = 5, 10, 5, 10
            
            If a value is missing on the left, fill it with `None`.
            `None` records the value already present in that position.

            self.my_button.margins = None, 10, None, 10
            self.my_button.margins = 5, None, None, 5
            self.my_button.margins = None, None, 5
            self.my_button.margins = None, None, None, 5
        """
        return (
            self._obj.property('topMargin'),
            self._obj.property('rightMargin'),
            self._obj.property('bottomMargin'),
            self._obj.property('leftMargin'))

    @margins.setter
    def margins(self, margins: tuple) -> None:
        prev_margins = self.margins

        if isinstance(margins, int) or isinstance(margins, str):
            top, right, bottom, left = (margins,) + prev_margins[1:]
        elif len(margins) == 2:
            top, right, bottom, left = margins + prev_margins[2:]
        elif len(margins) == 3:
            top, right, bottom, left = margins + (prev_margins[-1],)
        else:
            top, right, bottom, left = margins[:4]

        top = prev_margins[0] if not top else top
        right = prev_margins[1] if not right else right
        bottom = prev_margins[2] if not bottom else bottom
        left = prev_margins[3] if not left else left

        self._obj.setProperty('topMargin', top)
        self._obj.setProperty('rightMargin', right)
        self._obj.setProperty('bottomMargin', bottom)
        self._obj.setProperty('leftMargin', left)

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
