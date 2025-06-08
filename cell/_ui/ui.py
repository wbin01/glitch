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
    width: Math.min(contentItem.implicitWidth, Screen.width)
    height: Math.min(contentItem.implicitHeight, Screen.height)
    title: qsTr("App Mínimo")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    Rectangle {
        id: outerBorder
        objectName: "outerBorder"
        anchors.fill: parent
        color: "transparent"
        border.color: "#44000000"
        border.width: borderWidth
        radius: 11
        z: 0

        property int borderWidth: 1
    }

    Rectangle {
        id: mainRect
        objectName: "mainRect"
        width: 300
        height: 200
        radius: 10
        color: "#333"
        border.color: borderColor
        border.width: borderWidth
        anchors.margins: margins
        z: 1

        anchors.fill: parent
        //anchors.centerIn: parent

        property color borderColor: "#444"
        property bool isActive: true
        property int borderWidth: 1
        property int margins: 1

        //Behavior on radius {
        //    NumberAnimation {
        //        duration: 2000
        //        easing.type: Easing.InOutQuad
        //    }
        //}

        Rectangle {
            id: dragArea
            width: parent.width
            height: 40
            color: "#00000000"  // invisível
            MouseArea {
                anchors.fill: parent
                drag.target: mainRect

                onPressed: {
                    logic.start_move()
                }
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
            id: _columnLayout
            objectName: "_columnLayout"
            anchors.centerIn: parent
            spacing: 20

// **closing_key**

        }  // ColumnLayout id: _columnLayout

    }  // Rectangle id: mainRect

}  // Window id: window

"""

class Ui(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__('appFrame', *args, **kwargs)
        self.object_id = 'appFrame'
        self.qml = object_code
