#/usr/bin/env python3
from PySide6 import QtCore

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
import QtQuick.Controls
import QtQuick.Layouts

import "elements"


Window {
    id: window  // <id>
    objectName: "window"  // <objectName>
    property string qmlType: "Window"  // <className>

    // id: window
    visible: true
    visibility: Window.Windowed
    
    height: _height
    property int _height: 200
    
    width: _width
    property int _width: 200

    minimumWidth: 200
    minimumHeight: 200
    title: qsTr("Cell")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    Rectangle {
        id: outerBorder
        objectName: "outerBorder"
        anchors.fill: parent
        color: "transparent"
        border.color: "#44000000"
        border.width: 1
        radius: 11
        z: 0
    }

    Rectangle {
        id: mainRect
        objectName: "mainRect"
        anchors.fill: parent
        anchors.margins: margins
        radius: 10
        color: "#333"
        border.color: borderColor
        border.width: borderWidth
        z: 1

        property color borderColor: "#444"
        property bool isActive: true
        property int borderWidth: 1
        property int margins: 1

// MainFrame

        ColumnLayout {
            id: mainColumnLayout
            objectName: "mainColumnLayout"
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
        self.__spacing = 6

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
    def spacing(self) -> int:
        """..."""
        return self.__spacing

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        if self._obj:
            self._obj.findChild(
                QtCore.QObject, 'mainColumnLayout').setProperty(
                    'spacing', spacing)
        else:
            self._qml = self._qml.replace(
                f'spacing: {self.__spacing}', f'spacing: {spacing}')

        self.__spacing = spacing

    @property
    def style(self) -> dict:
        """..."""
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    @property
    def width(self) -> int:
        """..."""
        return self.__width

    @width.setter
    def width(self, width: int) -> None:
        if self._obj:
            self._obj.setProperty('_width', width)
        else:
            self._qml = self._qml.replace(
                f'_width: {self.__width}',
                f'_width: {width}')

        self.__width = width

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
