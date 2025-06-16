import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Window {
    id: window
    visible: true
    width: 200
    height: 200
    minimumWidth: 200
    minimumHeight: 200
    title: qsTr("App Mínimo")

    Rectangle {
        id: mainRect
        objectName: "mainRect"
        anchors.fill: parent
        color: "#333"
        border.width: 1
        border.color: "#888"
        z: 1

        ColumnLayout {
            id: mainColumnLayout
            objectName: "mainColumnLayout"
            anchors.fill: parent
            anchors.margins: 6
            spacing: 6
            clip: true

            Label {
                id: label
                objectName: "label"
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                // Layout.fillHeight: true
                text: "Hello"
            }

            Button {
                id: button
                objectName: "button"
                Layout.alignment: Qt.AlignHCenter
                Layout.fillWidth: true
                // Layout.fillHeight: true
                text: "Button"
            }

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
                    width: parent.width
                    spacing: 10


                    Button {
                        id: button0
                        objectName: "button0"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 0"
                    }

                    Button {
                        id: button1
                        objectName: "button1"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 1"
                    }

                    Button {
                        id: button2
                        objectName: "button2"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 2"
                    }

                    Button {
                        id: button3
                        objectName: "button3"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 3"
                    }

                    Button {
                        id: button4
                        objectName: "button4"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 4"
                    }

                    Button {
                        id: button5
                        objectName: "button5"
                        Layout.alignment: Qt.AlignHCenter
                        Layout.fillWidth: true
                        Layout.fillHeight: true
                        text: "Button 5"
                    }
                }
            }
        }
    }
}

