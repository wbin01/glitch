
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
            anchors.top: parent.top
            anchors.margins: 6
            spacing: 6
            clip: true
            Layout.fillHeight: false
            Layout.fillWidth: true


            Label {
                id: label
                objectName: "label"
                property string layoutType: "ColumnLayout"
                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment
                property bool fillWidth: true
                property bool fillHeight: true
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                property string topMargin: "0"
                property string rightMargin: "0"
                property string bottomMargin: "0"
                property string leftMargin: "0"
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin
                text: "Hello"
            // <property>
            } // Element id: label

            Button {
                id: button
                objectName: "button"
                property string layoutType: "ColumnLayout"
                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment
                property bool fillWidth: true
                property bool fillHeight: true
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                property string topMargin: "0"
                property string rightMargin: "0"
                property string bottomMargin: "0"
                property string leftMargin: "0"
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin
                text: "Button"
                iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
            // <property>
            } // Element id: button

            Button {
                id: button_m
                objectName: "button_m"
                property string layoutType: "ColumnLayout"
                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment
                property bool fillWidth: true
                property bool fillHeight: true
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                property string topMargin: "0"
                property string rightMargin: "0"
                property string bottomMargin: "0"
                property string leftMargin: "0"
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin
                text: "Button 00"
                iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
            // <property>
            } // Element id: button_m
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
                    id: button_0
                    objectName: "button_0"
                    property string layoutType: "ColumnLayout"
                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment
                    property bool fillWidth: true
                    property bool fillHeight: true
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    property string topMargin: "0"
                    property string rightMargin: "0"
                    property string bottomMargin: "0"
                    property string leftMargin: "0"
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin
                    text: "Button 0"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                // <property>
                } // Element id: button_0

                Button {
                    id: button_1
                    objectName: "button_1"
                    property string layoutType: "ColumnLayout"
                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment
                    property bool fillWidth: true
                    property bool fillHeight: true
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    property string topMargin: "0"
                    property string rightMargin: "0"
                    property string bottomMargin: "0"
                    property string leftMargin: "0"
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin
                    text: "Button 1"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                // <property>
                } // Element id: button_1

                Button {
                    id: button_2
                    objectName: "button_2"
                    property string layoutType: "ColumnLayout"
                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment
                    property bool fillWidth: true
                    property bool fillHeight: true
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    property string topMargin: "0"
                    property string rightMargin: "0"
                    property string bottomMargin: "0"
                    property string leftMargin: "0"
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin
                    text: "Button 2"
                    iconSource: "/home/user/Dev/github/cell/cell/static/icons/document-save.svg"
                // <property>
                } // Element id: button_2
                }
            
            }  // ScrollBox id: scroll
            
        

        }


    }
}

