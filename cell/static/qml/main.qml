
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "elements"


Window {
    id: window
    visible: true
    width: 200
    height: 200
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

            Label {
                id: label  // <id>
                objectName: "label"  // <objectName>
                property string qmlType: "Label"  // <className>
                text: "Hello"
                color: "#fff"
            }  // _136146985060640

            Button {
                id: button  // <id>
                objectName: "button"  // <objectName>
                property string qmlType: "Button"  // <className>
                text: "Button"
                iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
            }  // _136146985061120

            Button {
                id: button_m  // <id>
                objectName: "button_m"  // <objectName>
                property string qmlType: "Button"  // <className>
                text: "Button 00"
                iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
            }  // _136146985061168

            // ScrollBox
            ScrollView {
                Layout.fillWidth: true
                Layout.fillHeight: true
                clip: true
                contentWidth: availableWidth

                background: Rectangle {
                    color: "#22000000"
                    radius: 4
                }

                ColumnLayout {
                    id: scroll
                    objectName: "scroll"
                    property string qmlType: "ScrollBox"
                    // width: parent.width
                    // Layout.fillWidth: true
                    width: parent.width
                    spacing: 10

                Button {
                    id: button_0  // <id>
                    objectName: "button_0"  // <objectName>
                    property string qmlType: "Button"  // <className>
                    text: "Button 0"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                }  // _136146985060688

                Button {
                    id: button_1  // <id>
                    objectName: "button_1"  // <objectName>
                    property string qmlType: "Button"  // <className>
                    text: "Button 1"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                }  // _136146865978880

                Button {
                    id: button_2  // <id>
                    objectName: "button_2"  // <objectName>
                    property string qmlType: "Button"  // <className>
                    text: "Button 2"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                }  // _136146865978976

                Button {
                    id: button_3  // <id>
                    objectName: "button_3"  // <objectName>
                    property string qmlType: "Button"  // <className>
                    text: "Button 3"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                }  // _136146865979072

                Button {
                    id: button_4  // <id>
                    objectName: "button_4"  // <objectName>
                    property string qmlType: "Button"  // <className>
                    text: "Button 4"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                }  // _136146865979168

                Label {
                    id: _136146985061600  // <id>
                    objectName: "_136146985061600"  // <objectName>
                    property string qmlType: "Label"  // <className>
                    text: "Olá"
                    color: "#fff"
                }  // _136146985061600

                }
            
            }  // ScrollBox id: scroll
            

        }
    }
}

