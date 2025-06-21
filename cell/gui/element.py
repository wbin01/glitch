#/usr/bin/env python3
from PySide6 import QtQuick


class Element(object):
    """..."""
    def __init__(
            self, qt_quick_item: QtQuick.QQuickItem, *args, **kwargs) -> None:
        """..."""
        self.__obj = qt_quick_item
        self.object_id = '_' + str(id(self))
        self.__element_name = 'Element'
        self.__qml = ''

    @property
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        A tuple with the 4 margin values. The values are in clockwise
        order: top, right, bottom and left respectively.

        Get:
            (5, 10, 5, 10)

        Set:
            It is not mandatory to pass all the values, the last value will be 
            used to fill in the missing ones:

            `margins = 5` is equivalent to `margins = 5, 5, 5, 5`
            `margins = 5, 10` is equivalent to `margins = 5, 10, 10, 10`

            Use `None` for a value to be automatic. `None` indicates that the 
            value is the same as before. Example:

                # Change only the vertical margins (top and bottom)
                `margins = 10, None, 10, None`
        """
        return (
            self._obj.property('topMargin'),
            self._obj.property('rightMargin'),
            self._obj.property('bottomMargin'),
            self._obj.property('leftMargin'))

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            if not margins.isdigit():
                return
            margins = int(magins)

        prev_margins = self.margins

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = prev_margins[0] if top is None else top
        right = prev_margins[1] if right is None else right
        bottom = prev_margins[2] if bottom is None else bottom
        left = prev_margins[3] if left is None else left

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
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

    @property
    def _element_name(self) -> str:
        """..."""
        return self.__element_name

    @_element_name.setter
    def _element_name(self, element_name: str) -> None:
        self.__element_name = element_name

    @property
    def _obj(self) -> str:
        """..."""
        return self.__obj

    @_obj.setter
    def _obj(self, obj: str) -> None:
        self.__obj = obj
