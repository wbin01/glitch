import QtQuick 2.15
// import QtGraphicalEffects 1.15

Item {
    id: root
    property color backgroundColor: "#222"
    property color borderColor: "#666"
    property int borderWidth: 2
    property int radius: 12
    property int shadowSize: 16
    property color shadowColor: "#80000000"

    width: 300
    height: 200
    clip: false   // painel em si não precisa de clip; o fundo interno vai clipar

    // Sombra
    // Rectangle {
    //     id: shadow
    //     anchors.fill: parent
    //     anchors.margins: -root.shadowSize
    //     radius: root.radius + root.shadowSize
    //     color: "transparent"
    //     layer.enabled: true
    //     layer.effect: DropShadow {
    //         horizontalOffset: 0
    //         verticalOffset: 4
    //         radius: root.shadowSize
    //         samples: 32
    //         color: root.shadowColor
    //     }
    // }

    // Fundo com clip
    Rectangle {
        id: background
        anchors.fill: parent
        color: root.backgroundColor
        radius: root.radius
        border.color: root.borderColor
        border.width: root.borderWidth
        antialiasing: true
        clip: true    // **AQUI o conteúdo será recortado**
    }

    // Conteúdo do painel
    Item {
        id: content
        anchors.fill: background
        clip: true    // garante que qualquer filho também será recortado
    }
}
