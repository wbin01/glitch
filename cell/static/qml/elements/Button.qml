import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: button
    objectName: "button"
    property string qmlType: "Button"
    property color borderColor: "#555"
    property color backgroundColor: "#444"
    property alias iconSource: icon.source
    property bool isHovered: false
    property bool hasIcon: iconSource !== ""

    contentItem: Item {
        anchors.fill: parent

        Row {
            id: row
            spacing: 8
            anchors.centerIn: parent  // Centraliza o conteúdo

            Image {
                id: icon
                objectName: "icon"
                source: ""
                visible: icon.source !== ""
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                id: text
                objectName: "text"
                text: button.text
                color: "#ccc"
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    background: Rectangle {
        id: buttonBackground
        objectName: "buttonBackground"
        color: "#444"

        property color borderColor: "#444"
        border.color: background.borderColor

        border.width: 1
        radius: 6
    }

    implicitWidth: row.implicitWidth + 12
    implicitHeight: row.implicitHeight + 14
}
