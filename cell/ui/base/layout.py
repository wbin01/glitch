#/usr/bin/env python3
from .ui import UI
from ...enum import Orientation


class Layout(object):
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    pass


class Element(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    pass


layout = """
ColumnLayout {
    id: columnLayout  // <id>
    objectName: "columnLayout"  // <objectName>
    property string qmlType: "ColumnLayout"  // <className>
    spacing: 6
    
// **closing_key**
} // <suffix_id>
"""

row = """
RowLayout {
    id: rowLayout  // <id>
    objectName: "rowLayout"  // <objectName>
    property string qmlType: "RowLayout"  // <className>
    spacing: 6

// **closing_key**
} // <suffix_id>
"""


class Layout(UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(
            self, orientation: Orientation = Orientation.VERTICAL,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self._qml = layout if orientation == Orientation.VERTICAL else row
        self.id = '_' + str(id(self))
        self._element_type = 'Layout'

        self.__spacing = 6
        self.__items = []

    @property
    def spacing(self) -> int:
        """..."""
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
