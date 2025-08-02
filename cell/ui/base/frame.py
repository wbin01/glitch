#!/usr/bin/env python3
from PySide6 import QtCore

from .ui import UI
from ...enum import Orientation, FrameHint, FrameState
from ...platform_ import Style


class Layout(object):
    """Layout object.

    Organizes elements in stacks like a column or side by side like a row.
    """
    def __str__(self):
        return "<class 'Layout'>"


class Element(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __str__(self):
        return "<class 'Element'>"


qml = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "elements"


Window {
    id: frame  // <id>
    objectName: "frame"  // <objectName>
    property string qmlType: "Window"  // <className>
    property string baseClass: "Frame"  // <baseClass>

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

// Resize corners

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

qml_edges = """
// Resize corners
// Top left - resize NW
        MouseArea {
            id: resizeTopLeft
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.left: parent.left
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.LeftEdge)
        }

        // Top right - resize NE
        MouseArea {
            id: resizeTopRight
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.right: parent.right
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.RightEdge)
        }

        // Bottom left - resize SW
        MouseArea {
            id: resizeBottomLeft
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.LeftEdge)
        }

        // Bottom right - resize SE
        MouseArea {
            id: resizeBottomRight
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.RightEdge)
        }

        // Top - N
        MouseArea {
            id: resizeTop
            anchors.top: parent.top
            anchors.left: resizeTopLeft.right
            anchors.right: resizeTopRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge)
        }

        // Bottom - S
        MouseArea {
            id: resizeBottom
            anchors.bottom: parent.bottom
            anchors.left: resizeBottomLeft.right
            anchors.right: resizeBottomRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge)
        }

        // Left - W
        MouseArea {
            id: resizeLeft
            anchors.top: resizeTopLeft.bottom
            anchors.bottom: resizeBottomLeft.top
            anchors.left: parent.left
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.LeftEdge)
        }

        // Right - E
        MouseArea {
            id: resizeRight
            anchors.top: resizeTopRight.bottom
            anchors.bottom: resizeBottomRight.top
            anchors.right: parent.right
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.RightEdge)
        }
// Resize corners
"""


class Frame(UI):
    """An application frame.

    A frame where visual elements are inserted. Usually called a "Window".
    It is not the main Frame of an application, and it has no movement 
    capabilities. It is ideal as a part of the main application, such as a 
    context menu or a tool panel.
    """
    def __init__(self, resizable: bool = False, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = qml
        if resizable:
            qml_init, qml_end = qml.split('\n// Resize corners')
            self._qml = qml_init + qml_edges + qml_end

        self._element_type = 'Frame'

        self.__height = 200
        self.__width = 200
        self.__spacing = 6

        self.__frame_hint = FrameHint.FRAME
        self.__frame_state = FrameState.FRAME
        self.__items = []
        self.__style = Style().style
        self.__visibility = 'Window.Windowed'

    @property
    def frame_hint(self) -> FrameHint:
        """Frame behavior hint.

        FrameHint.BOTTOM → Always behind.
        FrameHint.FRAME → Normal behavior.
        FrameHint.POPUP → Popup Frame (does not appear in the taskbar).
        FrameHint.TOOL → Tool-like Frame (does not appear in the taskbar).
        FrameHint.TOP → Always on top.

        Use `FrameHint.TOOL` and `FrameHint.POPUP` inside a method to activate 
        them only when the window is ready; this will avoid styling issues.

        Use the `name` property to know which `FrameHint` it is.
        
        >>> self.frame_hint = FrameHint.FRAME
        >>> print(self.frame_hint.name)
        FRAME
        """
        return self.__frame_hint

    @frame_hint.setter
    def frame_hint(self, frame_hint: FrameHint) -> None:
        hints = {
            'BOTTOM': 'Qt.FramelessWindowHint | Qt.WindowStaysOnBottomHint',
            'FRAME': 'Qt.FramelessWindowHint',
            'POPUP': 'Qt.FramelessWindowHint | Qt.Popup',
            'TOOL': 'Qt.FramelessWindowHint | Qt.Tool',
            'TOP': 'Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint'}

        if self._obj:
            self._obj.setProperty('flags', int(frame_hint.value))
        else:
            self._qml = self._qml.replace(
                f'flags: {hints[self.__frame_hint.name]}',
                f'flags: {hints[frame_hint.name]}')

        self.__frame_hint = frame_hint

    @property
    def frame_state(self) -> FrameState:
        """The state of the Frame.

        A `FrameState` enum indicating whether the Frame is maximized, 
        minimized, full screen, in a normal frame or  hidden.
        """
        return self.__frame_state

    @frame_state.setter
    def frame_state(self, frame_state: FrameState = FrameState.FRAME) -> None:
        # Window.AutomaticVisibility  1     system default (normally Windowed)
        frame_state_value = {
            0: 'Window.Hidden', 1: 'Window.AutomaticVisibility',
            2: 'Window.Windowed', 3: 'Window.Minimized',
            4: 'Window.Maximized', 5: 'Window.FullScreen'}
        visibility = frame_state_value[frame_state.value]

        if self._obj:
            if frame_state.value == 2:
                self._obj.showNormal()
            elif frame_state.value == 4:
                self._obj.showMaximized()
            elif frame_state.value == 3:
                self._obj.showMinimized()
            elif frame_state.value == 5:
                self._obj.showFullScreen()
        else:
            self._qml = self._qml.replace(
                f'visibility: {self.__visibility}',
                f'visibility: {visibility}')

        self.__visibility = visibility
        self.__frame_state = frame_state

    @property
    def height(self) -> int:
        """Frame Height."""
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
        """Spacing Between Elements.

        The Frame contains a vertical Layout as a Column type, which manages 
        the position and spacing between Elements.
        """
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
        """Application style.

        A dictionary with color and style information for each visual element 
        in the application.
        """
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    @property
    def width(self) -> int:
        """Frame Width."""
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

    def __str__(self):
        return "<class 'Frame'>"
