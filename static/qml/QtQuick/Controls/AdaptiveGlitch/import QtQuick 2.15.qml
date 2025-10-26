import QtQuick 2.15
import QtQuick.Controls 2.15

import QtQuick 2.15
import QtQuick.Controls 2.15
// opcional, se quiser usar SvgImage:
// import QtSvg 1.1

ToolButton {
    id: frameCloseButton

    // use file:// para caminhos absolutos locais
    icon.source: "file:///home/user/Dev/github/glitch/static/control_button/plasma/window-close-b-symbolic.svg"

    // define um tamanho mínimo para testar
    width: 36
    height: 28
    padding: 6

    background: Rectangle {
        anchors.fill: parent
        radius: 6
        border.width: 0
        color: frameCloseButton.down ? "#ff323232"
             : frameCloseButton.hovered ? "#ff323232"
             : "#ff323232"
    }

    // contentItem com Image que dimensiona com base no tamanho do botão
    contentItem: Item {
        anchors.fill: parent

        Image {
            id: iconImg
            anchors.centerIn: parent
            // prefere usar icon.source, mas garante fallback:
            source: frameCloseButton.icon.source ? frameCloseButton.icon.source
                                                : "file:///home/user/Dev/github/glitch/static/control_button/plasma/window-close-b-symbolic.svg"
            // ajustar tamanho relativo ao botão
            width: Math.min(parent.width - frameCloseButton.padding*2, parent.height - frameCloseButton.padding*2)
            height: width
            fillMode: Image.PreserveAspectFit

            onStatusChanged: {
                console.log("iconImg.status =", status) // 0 = Null, 1 = Loading, 2 = Ready, 3 = Error
                if (status === Image.Error) {
                    console.log("Image error: ", source, iconImg.errorString)
                }
            }
        }
    }
}

