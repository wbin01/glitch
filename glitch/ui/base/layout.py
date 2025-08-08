#!/usr/bin/env python3
import logging

from PySide6 import QtCore

from .ui import UI
from ...enum import Orientation


column = """
ColumnLayout {
    id: column  // <id>
    objectName: "column"  // <objectName>
    property string qmlType: "Column"  // <className>
    property string baseClass: "Layout"  // <baseClass>
"""

row = """
RowLayout {
    id: row  // <id>
    objectName: "row"  // <objectName>
    property string qmlType: "Row"  // <className>
    property string baseClass: "Layout"  // <baseClass>
"""

properties = """
    spacing: 6

// **closing_key**
"""
# } close on UI


class Layout(object):
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    def __str__(self) -> str:
        return "<class 'Layout'>"


class Element(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __str__(self) -> str:
        return "<class 'Element'>"


class Layout(UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(
            self, orientation: Orientation = Orientation.VERTICAL,
            *args, **kwargs) -> None:
        """
        :param orientation: Layout orientation, VERTICAL or HORIZONTAL.
        """
        super().__init__(*args, **kwargs)
        # Set QML
        header = column if orientation == Orientation.VERTICAL else row
        self._qml = header + self._qml.split('// Element header')[1]
        self._qml = self._qml.replace('\n    // <property>', properties)

        # self._qml = layout_header if orientation == Orientation.VERTICAL else row_header
        self.id = '_' + str(id(self))
        self._element_type = 'Layout'

        self.__margins = 0, 0, 0, 0
        self.__spacing = 6
        self.__items = []

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
        if not isinstance(margins, int) and not isinstance(margins, tuple):
            logging.error(
                f'\n  {self._element_type}.margins: Use a tuple of integers '
                'like (10, 10, 10, 10) or an integer like 10.')
            return

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 1:
            top, right, bottom, left = (
                margins[0], margins[0], margins[0], margins[0])
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

    @property
    def spacing(self) -> int:
        """Spacing Between Elements."""
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        if self._obj:
            self._obj.setProperty('spacing', spacing)
        else:
            self._qml = self._qml.replace(
                f'spacing: {self.__spacing}', f'spacing: {spacing}')

        self.__spacing = spacing

    def add(self, obj: Layout | Element) -> Layout | Element:
        """Add items.

        Adds items such as Elements and Layouts to this Layout.
        
        :param obj: Element or Layout object type
        """
        if self._obj:
            obj._obj.setParentItem(self)
        else:
            setattr(self, obj.id, obj)

        self.__items.append(obj)
        return obj

    def items(self) -> list:
        """Items added to the Layout.

        List that includes Elements and other Layouts.
        """
        return self.__items

    def __str__(self) -> str:
        return "<class 'Layout'>"
