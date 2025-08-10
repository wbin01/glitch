#!/usr/bin/env python3
import logging

from PySide6 import QtCore

from .ui import UI
from ...enum import Orientation


column = """
ColumnLayout {
    id: column  // ID
    objectName: "column"  // Object name
    property string qmlType: "Column"  // Class Name
    property string baseClass: "Layout"  // Base class name
"""

row = """
RowLayout {
    id: row  // ID
    objectName: "row"  // Object name
    property string qmlType: "Row"  // Class Name
    property string baseClass: "Layout"  // Base class name
"""

# Layout goes in Item or Layout
# The "Layout.fillWidth" and "spacing" property will be set in the final Layout
properties = """
    // Layout header

    // Property

// Close
"""
# } close on UI
# Layout.minimumHeight
# Layout.maximumHeight


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
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    def __init__(
            self, orientation: Orientation = Orientation.VERTICAL,
            *args, **kwargs) -> None:
        """
        :param orientation: Layout orientation, VERTICAL or HORIZONTAL.
        """
        super().__init__(*args, **kwargs)
        # QML
        header = column if orientation == Orientation.VERTICAL else row
        self._qml = header + self._qml.split(
            '// Layout header')[1].replace('\n    // Property', properties)
        self.class_id('Layout')

        # Properties
        self.__spacing = 6
        self.__items = []

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

    def add(self, obj: Element | Layout) -> Element | Layout:
        """Add items.

        Adds items such as Elements and Layout to this Layout.
        
        :param obj: Element or Layout object type
        """
        if self._obj:
            obj._obj.setParentItem(self)
        else:
            setattr(self, obj._id, obj)

        self.__items.append(obj)
        return obj

    def items(self) -> list:
        """Items added to the Layout.

        List that includes Elements and other Layouts.
        """
        return self.__items

    def __str__(self) -> str:
        return "<class 'Layout'>"
