import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: control

    background: Rectangle {
        anchors.fill: parent
        color: control.down ? "#333080c7" :
               control.hovered ? "#ff3b3b3b" :
               "#ff3b3b3b"
        border.color: control.down ? "#993080c7" :
                      control.hovered ? "#993080c7" :
                      "#ff5e5e5e"
        border.width: 1
        radius: 3
    }
}