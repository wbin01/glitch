#!/usr/bin/env python3
from ..ui import UI


qml = """
    property string baseClass: "Element"  // <baseClass>
    height: 30
    width: 100
    // <property>
"""


class Element(UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = self._qml.replace('\n    // <property>', qml)
        self._element_type = 'Element'

        self.__margins = 0, 0, 0, 0

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

                # Change vertical margins (top and bottom)
                `element.margins = 10, None, 10, None`

                # Change horizontal margins (right and left)
                `element.margins = None, 5, None, 5`
        """
        return self.__margins

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            if not margins.isdigit():
                return
            margins = int(margins)

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = self.__margins[0] if top is None else top
        right = self.__margins[1] if right is None else right
        bottom = self.__margins[2] if bottom is None else bottom
        left = self.__margins[3] if left is None else left

        if self._obj:
            self._obj.setProperty('topMargin', top)
            self._obj.setProperty('rightMargin', right)
            self._obj.setProperty('bottomMargin', bottom)
            self._obj.setProperty('leftMargin', left)
        else:
            self._qml = self._qml.replace(
                f'property int topMargin: {self.__margins[0]}',
                f'property int topMargin: {top}')
            self._qml = self._qml.replace(
                f'property int rightMargin: {self.__margins[1]}',
                f'property int rightMargin: {right}')
            self._qml = self._qml.replace(
                f'property int bottomMargin: {self.__margins[2]}',
                f'property int bottomMargin: {bottom}')
            self._qml = self._qml.replace(
                f'property int leftMargin: {self.__margins[3]}',
                f'property int leftMargin: {left}')

        self.__margins = top, left, bottom, right

    def __str__(self) -> str:
        return "<class 'Element'>"
