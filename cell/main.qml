import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "components"


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

        // Canto superior esquerdo - resize diagonal NW
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

        // Canto superior direito - resize diagonal NE
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

        // Canto inferior esquerdo - resize diagonal SW
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

        // Canto inferior direito - resize diagonal SE
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

        // Borda superior
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

        // Borda inferior
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

        // Borda esquerda
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

        // Borda direita
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
            id: columnLayout
            objectName: "columnLayout"
            anchors.centerIn: parent
            spacing: 20

            Label {
                id: label
                objectName: "label"
                text: "Olá, mundo!"
                color: "#EEE"
                // font.pointSize: 16
                horizontalAlignment: Text.AlignHCenter
                Layout.alignment: Qt.AlignHCenter
            }

            Button {
                id: btn0
                objectName: "btn0"
                text: "Clique aqui"
                iconSource: "../icons/document-save.svg"
            }
            Button {
                id: btn01
                objectName: "btn01"
                text: "Item 1"
                iconSource: "../icons/document-save.svg"
            }
            
            Button {
                id: btn02
                objectName: "btn02"
                text: "Item 2"
                iconSource: "../icons/document-save.svg"
            }

            // *** ScrollView
            Rectangle {
                width: 200
                height: 100
                color: "#11000000" // "transparent"
                Layout.alignment: Qt.AlignHCenter

                ScrollView {
                    anchors.fill: parent
                    clip: true
                    anchors.leftMargin: 5
                    anchors.rightMargin: 5
                    anchors.topMargin: 0
                    anchors.bottomMargin: 0
                    // ScrollBar.vertical.policy: ScrollBar.AlwaysOn

                    Column {
                        width: parent.width
                        spacing: 10

                        Button {
                            text: "Item 1"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 2"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 3"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 4"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 5"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 6"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 7"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 8"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 9"
                            iconSource: "../icons/document-save.svg"
                            }
                        Button {
                            text: "Item 10"
                            iconSource: "../icons/document-save.svg"
                            }
                    }
                }
            }

            Button {
                text: "Outro botão"
                Layout.alignment: Qt.AlignHCenter
            }

            // ScrollView ***
        }
    }

}
