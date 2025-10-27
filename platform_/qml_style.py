#!/usr/bin/env python3


qml_style = """
import QtQuick
import QtQuick.Controls
// sep imports-elements
// +
MainFrame {
    title: qsTr("UI")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    width: 400
    height: 400

    minimumWidth: 100
    minimumHeight: 30

    visible: true
    visibility: Window.Windowed

    property alias borderWidth: mainRectangle.borderWidth
    property alias outLineWidth: mainRectangle.outLineWidth
    property alias outLineColor: mainRectangle.outLineColor
    property alias backgroundColor: mainRectangle.backgroundColor
    property alias borderColor: mainRectangle.borderColor

    property alias radiusTopLeft: mainRectangle.radiusTopLeft
    property alias radiusTopRight: mainRectangle.radiusTopRight
    property alias radiusBottomRight: mainRectangle.radiusBottomRight
    property alias radiusBottomLeft: mainRectangle.radiusBottomLeft

    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.RightButton
        onPressed: logic.connections()
    }

    Rectangle {
        id: mainRectangle
        objectName: "mainRectangle"
        anchors.fill: parent
        color: "transparent"
        z: 1
        property bool isActive: true

        property color backgroundColor: "[MainFrame]background_color"
        property color borderColor: "[MainFrame]border_color"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: [MainFrame]border_radius_tl
        property int radiusTopRight: [MainFrame]border_radius_tr
        property int radiusBottomRight: [MainFrame]border_radius_br
        property int radiusBottomLeft: [MainFrame]border_radius_bl

        Canvas {
            id: canvas
            objectName: "canvas"
            anchors.fill: parent
            property int borderSpacing: 1

            onPaint: {
                var ctx = getContext("2d");
                ctx.clearRect(0, 0, width, height);

                // Function to draw rounded rectangle with individuals corners
                function roundedRect(x, y, w, h, rtl, rtr, rbr, rbl) {
                    ctx.beginPath();
                    ctx.moveTo(x + rtl, y);
                    ctx.lineTo(x + w - rtr, y);
                    ctx.arcTo(x + w, y, x + w, y + rtr, rtr);
                    ctx.lineTo(x + w, y + h - rbr);
                    ctx.arcTo(x + w, y + h, x + w - rbr, y + h, rbr);
                    ctx.lineTo(x + rbl, y + h);
                    ctx.arcTo(x, y + h, x, y + h - rbl, rbl);
                    ctx.lineTo(x, y + rtl);
                    ctx.arcTo(x, y, x + rtl, y, rtl);
                    ctx.closePath();
                }

                // --- Background ---
                roundedRect(
                    1, 1, width - 2, height - 2,
                    mainRectangle.radiusTopLeft,
                    mainRectangle.radiusTopRight,
                    mainRectangle.radiusBottomRight,
                    mainRectangle.radiusBottomLeft);

                ctx.fillStyle = mainRectangle.backgroundColor;
                ctx.fill();

                // --- Outer border ---
                roundedRect(
                    0, 0, width, height,
                    mainRectangle.radiusTopLeft + 2,
                    mainRectangle.radiusTopRight + 2,
                    mainRectangle.radiusBottomRight + 2,
                    mainRectangle.radiusBottomLeft + 2);

                ctx.strokeStyle = mainRectangle.outLineColor;
                ctx.lineWidth = mainRectangle.outLineWidth;
                ctx.stroke();

                // --- Inner border ---
                var inset = borderSpacing + mainRectangle.borderWidth / 2;
                roundedRect(
                    inset, inset,
                    width - inset * 2,
                    height - inset * 2,
                    Math.max(0, mainRectangle.radiusTopLeft - inset),
                    Math.max(0, mainRectangle.radiusTopRight - inset),
                    Math.max(0, mainRectangle.radiusBottomRight - inset),
                    Math.max(0, mainRectangle.radiusBottomLeft - inset));

                ctx.strokeStyle = mainRectangle.borderColor;
                ctx.lineWidth = mainRectangle.borderWidth;
                ctx.stroke();
            }
        }

        // Drag area
        Rectangle {
            id: dragArea
            objectName: "dragArea"
            height: 20
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
                margins: 5  // margem de 10px nas laterais
            }
            color: "transparent"
            z: 0

            MouseArea {
                anchors.fill: parent
                // drag.target: // id
                onPressed: logic.start_move()
            }
        }
        // Drag area


        // Resize corners
        // Top left - resize NW
        MouseArea {
            id: resizeTopLeft
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.left: parent.left
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.LeftEdge)
        }

        // Top right - resize NE
        MouseArea {
            id: resizeTopRight
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.right: parent.right
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge | Qt.RightEdge)
        }

        // Bottom left - resize SW
        MouseArea {
            id: resizeBottomLeft
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            cursorShape: Qt.SizeBDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.LeftEdge)
        }

        // Bottom right - resize SE
        MouseArea {
            id: resizeBottomRight
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            cursorShape: Qt.SizeFDiagCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge | Qt.RightEdge)
        }

        // Top - N
        MouseArea {
            id: resizeTop
            anchors.top: parent.top
            anchors.left: resizeTopLeft.right
            anchors.right: resizeTopRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.TopEdge)
        }

        // Bottom - S
        MouseArea {
            id: resizeBottom
            anchors.bottom: parent.bottom
            anchors.left: resizeBottomLeft.right
            anchors.right: resizeBottomRight.left
            height: 5
            cursorShape: Qt.SizeVerCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.BottomEdge)
        }

        // Left - W
        MouseArea {
            id: resizeLeft
            anchors.top: resizeTopLeft.bottom
            anchors.bottom: resizeBottomLeft.top
            anchors.left: parent.left
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.LeftEdge)
        }

        // Right - E
        MouseArea {
            id: resizeRight
            anchors.top: resizeTopRight.bottom
            anchors.bottom: resizeBottomRight.top
            anchors.right: parent.right
            width: 5
            cursorShape: Qt.SizeHorCursor
            hoverEnabled: true
            onPressed: logic.start_resize(Qt.RightEdge)
        }
        // Resize corners

        ColumnLayout {
            id: mainColumnLayout
            objectName: "mainColumnLayout"
            anchors.fill: parent
            anchors.margins: 4
            spacing: 6
            clip: true
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: true
        }
    }
    default property alias content: mainColumnLayout.data
}
// +
Button {
    id: button

    background: Rectangle {
        anchors.fill: parent

        color:
            button.checked && button.hovered ?
                "[Button:checked:hover]background_color" :
            button.checked ?
                "[Button:checked]background_color" :
            button.down ?
                "[Button:clicked]background_color" :
            button.hovered ?
                "[Button:hover]background_color" : "[Button]background_color"

        border.color:
            button.checked && button.hovered ?
                "[Button:checked:hover]border_color" :
            button.checked ?
                "[Button:checked]border_color" :
            button.down ?
                "[Button:clicked]border_color" :
            button.hovered ?
                "[Button:hover]border_color" : "[Button]border_color"

        border.width: [Button]border_width
        radius: [Button]border_radius
    }
}
// +
FrameCloseButton {
    id: frameCloseButton
    property url normalIcon: "[FrameCloseButton]icon"
    property url hoverIcon: "[FrameCloseButton:hover]icon"
    property url clickedIcon: "[FrameCloseButton:clicked]icon"

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
                "[FrameCloseButton:clicked]background_color" :
            frameCloseButton.hovered ?
                "[FrameCloseButton:hover]background_color" :
                "[FrameCloseButton]background_color"

        border.color:
            frameCloseButton.down ?
                "[FrameCloseButton:clicked]border_color" :
            frameCloseButton.hovered ?
                "[FrameCloseButton:hover]border_color" :
                "[FrameCloseButton]border_color"

        border.width: [FrameCloseButton]border_width
        radius: [FrameCloseButton]border_radius
    }
}
// +
FrameMaxButton {
    id: frameMaxButton
    property url normalIcon: "[FrameMaxButton]icon"
    property url hoverIcon: "[FrameMaxButton:hover]icon"
    property url clickedIcon: "[FrameMaxButton:clicked]icon"

    icon.source:
        frameMaxButton.down ?
            clickedIcon :
        frameMaxButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            frameMaxButton.down ?
                "[FrameMaxButton:clicked]background_color" :
            frameMaxButton.hovered ?
                "[FrameMaxButton:hover]background_color" :
                "[FrameMaxButton]background_color"

        border.color:
            frameMaxButton.down ?
                "[FrameMaxButton:clicked]border_color" :
            frameMaxButton.hovered ?
                "[FrameMaxButton:hover]border_color" :
                "[FrameMaxButton]border_color"

        border.width: [FrameMaxButton]border_width
        radius: [FrameMaxButton]border_radius
    }
}
// +
ToolButton {
    id: toolButton

    background: Rectangle {
        anchors.fill: parent

        color:
            toolButton.checked && toolButton.hovered ?
                "[ToolButton:checked:hover]background_color" :
            toolButton.checked ?
                "[ToolButton:checked]background_color" :
            toolButton.down ?
                "[ToolButton:clicked]background_color" :
            toolButton.hovered ?
                "[ToolButton:hover]background_color" : "[ToolButton]background_color"

        border.color:
            toolButton.checked && toolButton.hovered ?
                "[ToolButton:checked:hover]border_color" :
            toolButton.checked ?
                "[ToolButton:checked]border_color" :
            toolButton.down ?
                "[ToolButton:clicked]border_color" :
            toolButton.hovered ?
                "[ToolButton:hover]border_color" : "[ToolButton]border_color"

        border.width: [ToolButton]border_width
        radius: [ToolButton]border_radius
    }
}
// +
Label {
    id: label
    color: "[Label]font_color"
}
"""


class QmlStyle(object):
    """..."""
    def __init__(self, style: dict, qml_path: str) -> None:
        """

        :param style: ...
        """
        self.__style = style
        self.__qml_path = qml_path / 'QtQuick' / 'Controls' / 'AdaptiveGlitch'
        self.__qml_style = qml_style

    def build(self) -> None:
        for style_header, style_key in self.__style.items():
            for key, value in style_key.items():
                mark = style_header + key
                if mark == '[MainFrame]border_radius':
                    for val, edge in zip(
                            value.split(','), ('tl', 'tr', 'br', 'bl')):
                        self.__qml_style = self.__qml_style.replace(
                            '[MainFrame]border_radius_' + edge, val.strip())
                else:
                    self.__qml_style = self.__qml_style.replace(mark, value)

        imports, themes = self.__qml_style.split('// sep imports-elements')
        for theme in themes.split('// +'):
            if not theme.strip():
                continue

            element_name = theme.strip().split('\n')[0].rstrip('{').strip()

            imports_add = ''
            if element_name in ('Window', 'MainFrame', 'Frame'):
                imports_add = 'import QtQuick.Layouts\n'

            for flip in (
                    ('FrameCloseButton', 'ToolButton'),
                    ('FrameMaxButton', 'ToolButton'),
                    ('MainFrame', 'Window')):
                theme = theme.replace(flip[0] + ' {', flip[1] + ' {')

            element_theme = imports.lstrip() + imports_add + theme
            element_theme_path = self.__qml_path / (element_name + '.qml')

            element_theme_path.write_text(element_theme)
