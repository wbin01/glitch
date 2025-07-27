#/usr/bin/env python3
from .layout import Layout
from ..platform.style import Style


object_code = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "elements"


Window {
    id: window
    visible: true
    visibility: Window.Windowed
    height: _height
    property int _height: 200
    width: 200
    minimumWidth: 200
    minimumHeight: 200
    title: qsTr("App Mínimo")
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

        // Drag area
        Rectangle {
            id: dragArea
            objectName: "dragArea"
            // width: parent.width
            // width: parent.width - 20
            height: 40
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
                margins: 5  // margem de 10px nas laterais
            }
            color: "transparent"
            z: 2

            MouseArea {
                anchors.fill: parent
                drag.target: mainRect
                onPressed: logic.start_move()
            }
        }

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

class MainFrame(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__('AppFrame', *args, **kwargs)
        self.object_id = 'appFrame'
        self._qml = object_code
        self.__style = Style().style

        self.__height = 200
        self.__width = 200
        self.__maximized = False
        self.__visibility = 'Window.Windowed'

    @property
    def style(self) -> dict:
        """..."""
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    @property
    def height(self) -> int:
        """..."""
        return self.__height

    @height.setter
    def height(self, height: int) -> None:
        if self._obj:
            self._obj.setProperty('_height', height)
            self.__height = height
            return
        
        qml_height = f'_height: {self.__height}'
        self.__height = height
        new_qml_height = f'_height: {self.__height}'

        self._qml = self._qml.replace(qml_height, new_qml_height)

    @property
    def maximized(self) -> bool:
        """..."""
        return self.__maximized

    @maximized.setter
    def maximized(self, maximized: bool) -> None:
        if self._obj:
            if maximized:
                self._obj.showMaximized()
            else:
                self._obj.showNormal()
            self.__maximized = maximized
            return

        qml = f'visibility: {self.__visibility}'
        self.__visibility = (
            'Window.Maximized' if maximized else 'Window.Windowed')
        new_qml = f'visibility: {self.__visibility}'

        self._qml = self._qml.replace(qml, new_qml)
        self.__maximized = maximized
