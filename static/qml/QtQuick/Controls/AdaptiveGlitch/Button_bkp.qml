import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: control

    // Background customizado
    background: Rectangle {
        anchors.fill: parent
        color: control.down ? "#404040" :
               control.hovered ? "#505050" : "#2d2d2d"
        border.color: control.focus ? "#5e9cff" : "#444"
        border.width: 1
        radius: 6
    }

    // Conteúdo: ícone + texto
    // contentItem: Row {
    //     anchors.centerIn: parent
    //     spacing: 6
    //     Image { id: iconItem; width: 16; height: 16; visible: source !== "" }
    //     Text { id: label; text: control.text; color: "#e0e0e0" }
    // }

    contentItem: Row {
        anchors.centerIn: parent
        spacing: 6

        Image {
            id: iconItem
            width: 16
            height: 16
            fillMode: Image.PreserveAspectFit
            visible: source !== "" && source !== null
        }

        Text {
            id: label
            text: control.text
            color: "#e0e0e0"
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

}
