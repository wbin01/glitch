import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: control
    text: "Botão"
    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"

    background: Rectangle {
        anchors.fill: parent
        color: control.down ? "#404040" :
               control.hovered ? "#505050" : "#2d2d2d"
        border.color: control.down ? "#5e9cff" :
                      control.hovered ? "#666" :
                      "#444"
        border.width: 1
        radius: 6
    }
}
