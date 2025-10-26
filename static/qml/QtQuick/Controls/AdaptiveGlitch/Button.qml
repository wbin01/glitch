import QtQuick 2.15
import QtQuick.Controls 2.15

Button {
    id: button

    background: Rectangle {
        anchors.fill: parent

        color:
            button.checked && button.hovered ?
                "#AA5e5e5e" :
            button.checked ?
                "#AA5e5e5e" :
            button.down ?
                "#33277094" :
            button.hovered ?
                "#ff3b3b3b" : "#ff3b3b3b"

        border.color:
            button.checked && button.hovered ?
                "#99277094" :
            button.checked ?
                "#ff5e5e5e" :
            button.down ?
                "#99277094" :
            button.hovered ?
                "#99277094" : "#ff5e5e5e"

        border.width: 1
        radius: 6
    }
}