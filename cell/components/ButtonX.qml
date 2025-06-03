import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: root
    property color borderColor: "#555"
    property color backgroundColor: "#444"
    property alias iconSource: icon.source
    property bool isHovered: false
    property bool hasIcon: iconSource !== ""

    //signal hoveredEntered()
    //signal hoveredExited()

    contentItem: Row {
        id: row
        spacing: 8
        // anchors.centerIn: parent
        anchors.fill: parent
        anchors.margins: 6  // metade de 12 para manter o padding
        // anchors.verticalCenter: parent.verticalCenter
        // anchors.horizontalCenter: parent.horizontalCenter

        Image {
            id: icon
            objectName: "icon"
            source: ""
            visible: icon.source !== ""
            //width: 16
            //height: 16
            fillMode: Image.PreserveAspectFit
            anchors.verticalCenter: parent.verticalCenter
        }

        Text {
            id: text
            objectName: "text"
            text: root.text
            color: root.down ? "#aaa" : root.hovered ? "white" : "#ccc"
            anchors.verticalCenter: parent.verticalCenter
        }
    }

    background: Rectangle {
        id: backgroundId
        objectName: "backgroundId"
        color: root.down ? "#333" : root.hovered ? "#555" : "#444"

        property color borderColor: "#444"
        border.color: background.borderColor

        border.width: 1
        radius: 6
    }

    implicitWidth: row.implicitWidth + 12
    implicitHeight: row.implicitHeight + 14

}
