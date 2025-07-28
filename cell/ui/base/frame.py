#/usr/bin/env python3
from .ui import UI
from ...enum.orientation import Orientation
from ...platform.style import Style


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


qml = """
import QtQuick
import QtQuick.Window

Window {
    id: contextWindow
    width: 200
    height: _height
    property int _height: 50
    visible: true
    flags: Qt.Popup
    color: "white"
    Rectangle {
        anchors.fill: parent
        border.color: "black"
        Text {
            anchors.centerIn: parent
            text: "Frame"
        }

        ColumnLayout {
            id: columnLayout
            objectName: "columnLayout"
            anchors.fill: parent
            // anchors.top: parent.top
            anchors.margins: 6
            spacing: 6
            clip: true
            // Layout.fillHeight: false
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true

// **closing_key**

        }
    }
}

"""
class Frame(UI):
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
        self._qml = qml
        self.__height = 200
        self.__width = 200
        self.__style = Style().style
        self.__items = []

    @property
    def height(self) -> int:
        """..."""
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        if self._obj:
            self._obj.setProperty('_height', height)
        else:
            self._qml = self._qml.replace(
                f'_height: {self.__height}',
                f'_height: {height}')

        self.__height = height

    @property
    def style(self) -> dict:
        """..."""
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

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
