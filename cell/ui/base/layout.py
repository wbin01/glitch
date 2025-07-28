#/usr/bin/env python3
from .ui import UI
from ...enum.orientation import Orientation


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
    id: columnLayout
    objectName: "columnLayout"
            
// **closing_key**
}
"""
row = """
RowLayout {
    id: rowLayout
    objectName: "rowLayout"
            
// **closing_key**
}
"""


class Layout(UI):
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    def __init__(
            self, orientation: Orientation = Orientation.VERTICAL,
            *args, **kwargs) -> None:
        """The init receives a Orientation Enum.

        `Orientation.VERTICAL` is the default.

        :param orientation: Orientation.VERTICAL or Orientation.HORIZONTAL.
        """
        super().__init__(*args, **kwargs)
        self._qml = layout if orientation == Orientation.VERTICAL else row
        self.__items = []

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
