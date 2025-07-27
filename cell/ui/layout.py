#/usr/bin/env python3
from ..enum.orientation import Orientation


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


class Layout(Layout):
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
        self.__id = '_' + str(id(self))
        self.__qml = layout if orientation == Orientation.VERTICAL else row
        self.__items = []
        self.__obj = None

    @property
    def id(self) -> str:
        """Layout identifier."""
        if self._obj:
            return self._obj.property('id')
        return self.__id

    @id.setter
    def id(self, id: str) -> None:
        if self._obj:
            self._obj.setProperty('id', id)
            self._obj.setProperty('objectName', id)
        else:
            self.__qml = self.__qml.replace(
                f'id: {self.__id}', f'id: {id}').replace(
                f'objectName: "{self.__id}"', f'objectName: "{id}"')

        self.__id = id

    @property
    def _obj(self) -> str:
        """Qt Object.

        Internal object manipulated by the wrapper class.
        """
        return self.__obj

    @_obj.setter
    def _obj(self, obj: str) -> None:
        self.__obj = obj

    @property
    def _qml(self) -> str:
        """Qml code.

        Internal Qml handled by the wrapper class.
        """
        return self.__qml

    @_qml.setter
    def _qml(self, qml: str) -> None:
        self.__qml = qml

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
