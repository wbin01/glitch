#/usr/bin/env python3
from .layout import Layout


object_code = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "elements"

Window {
    id: window
    visible: true
    width: 400
    height: 300
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

        // MouseArea para arrastar janela
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

        // Redimensionamento (bordas e cantos)
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
            id: _columnLayout
            objectName: "_columnLayout"
            anchors.fill: parent
            anchors.margins: 20
            spacing: 20

// **closing_key**
        }
    }
}

"""


class Ui(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__('appFrame', *args, **kwargs)
        self.object_id = 'appFrame'
        self.qml = object_code
