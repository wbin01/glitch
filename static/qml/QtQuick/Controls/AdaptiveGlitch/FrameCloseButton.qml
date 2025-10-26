import QtQuick
import QtQuick.Controls

ToolButton {
    id: frameCloseButton
    property url normalIcon: "/home/user/Dev/github/glitch/static/control_button/plasma/window-close-b-symbolic.svg"
    property url hoverIcon: "/home/user/Dev/github/glitch/static/control_button/plasma/window-close-hover-symbolic.svg"
    property url clickedIcon: "/home/user/Dev/github/glitch/static/control_button/plasma/window-close-clicked.svg"

    icon.source:
        frameCloseButton.down ?
            clickedIcon :
        frameCloseButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            frameCloseButton.down ?
                "#ff323232" :
            frameCloseButton.hovered ?
                "#ff323232" :
                "#ff323232"

        border.color:
            frameCloseButton.down ?
                "#ff323232" :
            frameCloseButton.hovered ?
                "#ff323232" :
                "#ff323232"

        border.width: 0
        radius: 6
    }
}
