import QtQuick 2.15
import QtQuick.Controls 2.15

ToolButton {
    id: toolButton

    background: Rectangle {
        anchors.fill: parent

        color:
            toolButton.checked && toolButton.hovered ?
                "#885e5e5e" :
            toolButton.checked ?
                "#885e5e5e" :
            toolButton.down ?
                "#33277094" :
            toolButton.hovered ?
                "#ff323232" : "#ff323232"

        border.color:
            toolButton.checked && toolButton.hovered ?
                "#99277094" :
            toolButton.checked ?
                "#ff5e5e5e" :
            toolButton.down ?
                "#99277094" :
            toolButton.hovered ?
                "#99277094" : "#ff323232"

        border.width: 1
        radius: 6
    }
}