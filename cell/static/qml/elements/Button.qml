import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

// import QtQuick 2.15
// import QtQuick.Controls 2.15
// import QtQuick.Layouts 1.15


Button {
    id: button  // <id>
    objectName: "button"  // <objectName>
    property string qmlType: "Button"  // <className>
    property string baseClass: "Button"  // <baseClass>
    property color borderColor: "#555"
    property color backgroundColor: "#444"
    property alias iconSource: icon.source
    property bool isHovered: false
    property bool hasIcon: iconSource !== ""

    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin
    hoverEnabled: true

    Layout.fillHeight: false
    Layout.preferredHeight: _height
    property int _height: 30

    Layout.fillWidth: true
    Layout.preferredWidth: _width
    property int _width: 100

    contentItem: Item {
        anchors.fill: parent

        Row {
            id: row
            spacing: 8
            anchors.centerIn: parent  // Center content

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
        id: background
        objectName: "background"

        property color backgroundColor: "#444"
        color: background.backgroundColor

        property color borderColor: "#444"
        border.color: background.borderColor

        border.width: 1
        radius: 6
    }

}
