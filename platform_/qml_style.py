#!/usr/bin/env python3


qml_style = """
import QtQuick
import QtQuick.Controls
// sep imports-elements
// +
Window {
    title: "Glitch App"
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

    property alias spacing: mainColumnLayout.spacing
    property alias borderSpacing: canvas.borderSpacing

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

        property color backgroundColor: "[AppFrame]background_color"
        property color borderColor: "[AppFrame]border_color"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: [AppFrame]border_radius_tl
        property int radiusTopRight: [AppFrame]border_radius_tr
        property int radiusBottomRight: [AppFrame]border_radius_br
        property int radiusBottomLeft: [AppFrame]border_radius_bl

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
            anchors.fill: parent
            anchors.margins: 1
            spacing: 6
            clip: true
        }
    }
    default property alias content: mainColumnLayout.data
}
// +
ScrollView {
    id: scroll
    Layout.fillWidth: true
    Layout.fillHeight: true

    clip: true
    contentWidth: availableWidth

    background: Rectangle {
        color: "#1E000000"
        radius: 4
    }

    ColumnLayout {
        id: scrollColumnLayout
        width: parent.width
        spacing: 6
    }
    default property alias content: scrollColumnLayout.data
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
CloseButton {
    id: appCloseButton
    padding: 0
    property url normalIcon: "[AppCloseButton]icon"
    property url hoverIcon: "[AppCloseButton:hover]icon"
    property url clickedIcon: "[AppCloseButton:clicked]icon"

    icon.source:
        appCloseButton.down ?
            clickedIcon :
        appCloseButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            appCloseButton.down ?
                "[AppCloseButton:clicked]background_color" :
            appCloseButton.hovered ?
                "[AppCloseButton:hover]background_color" :
                "[AppCloseButton]background_color"

        border.color:
            appCloseButton.down ?
                "[AppCloseButton:clicked]border_color" :
            appCloseButton.hovered ?
                "[AppCloseButton:hover]border_color" :
                "[AppCloseButton]border_color"

        border.width: [AppCloseButton]border_width
        radius: [AppCloseButton]border_radius
    }
}
// +
FullButton {
    id: appFullButton
    padding: 0
    property url normalIcon: "[AppFullButton]icon"
    property url hoverIcon: "[AppFullButton:hover]icon"
    property url clickedIcon: "[AppFullButton:clicked]icon"

    property url restoreNormalIcon: "[AppFullButton]restore_icon"
    property url restoreHoverIcon: "[AppFullButton:hover]restore_icon"
    property url restoreClickedIcon: "[AppFullButton:clicked]restore_icon"

    icon.source:
        appFullButton.down ?
            clickedIcon :
        appFullButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            appFullButton.down ?
                "[AppFullButton:clicked]background_color" :
            appFullButton.hovered ?
                "[AppFullButton:hover]background_color" :
                "[AppFullButton]background_color"

        border.color:
            appFullButton.down ?
                "[AppFullButton:clicked]border_color" :
            appFullButton.hovered ?
                "[AppFullButton:hover]border_color" :
                "[AppFullButton]border_color"

        border.width: [AppFullButton]border_width
        radius: [AppFullButton]border_radius
    }
}
// +
MaxButton {
    id: appMaxButton
    padding: 0
    property url normalIcon: "[AppMaxButton]icon"
    property url hoverIcon: "[AppMaxButton:hover]icon"
    property url clickedIcon: "[AppMaxButton:clicked]icon"

    property url restoreNormalIcon: "[AppMaxButton]restore_icon"
    property url restoreHoverIcon: "[AppMaxButton:hover]restore_icon"
    property url restoreClickedIcon: "[AppMaxButton:clicked]restore_icon"

    icon.source:
        appMaxButton.down ?
            clickedIcon :
        appMaxButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            appMaxButton.down ?
                "[AppMaxButton:clicked]background_color" :
            appMaxButton.hovered ?
                "[AppMaxButton:hover]background_color" :
                "[AppMaxButton]background_color"

        border.color:
            appMaxButton.down ?
                "[AppMaxButton:clicked]border_color" :
            appMaxButton.hovered ?
                "[AppMaxButton:hover]border_color" :
                "[AppMaxButton]border_color"

        border.width: [AppMaxButton]border_width
        radius: [AppMaxButton]border_radius
    }
}
// +
MinButton {
    id: appMinButton
    padding: 0
    property url normalIcon: "[AppMinButton]icon"
    property url hoverIcon: "[AppMinButton:hover]icon"
    property url clickedIcon: "[AppMinButton:clicked]icon"

    icon.source:
        appMinButton.down ?
            clickedIcon :
        appMinButton.hovered ?
            hoverIcon : normalIcon

    icon.width: undefined
    icon.height: undefined

    background: Rectangle {
        anchors.fill: parent

        color:
            appMinButton.down ?
                "[AppMinButton:clicked]background_color" :
            appMinButton.hovered ?
                "[AppMinButton:hover]background_color" :
                "[AppMinButton]background_color"

        border.color:
            appMinButton.down ?
                "[AppMinButton:clicked]border_color" :
            appMinButton.hovered ?
                "[AppMinButton:hover]border_color" :
                "[AppMinButton]border_color"

        border.width: [AppMinButton]border_width
        radius: [AppMinButton]border_radius
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
                if mark == '[AppFrame]border_radius':
                    for val, edge in zip(
                            value.split(','), ('tl', 'tr', 'br', 'bl')):
                        self.__qml_style = self.__qml_style.replace(
                            '[AppFrame]border_radius_' + edge, val.strip())
                else:
                    self.__qml_style = self.__qml_style.replace(mark, value)

        imports, themes = self.__qml_style.split('// sep imports-elements')
        for theme in themes.split('// +'):
            if not theme.strip():
                continue

            element_name = theme.strip().split('\n')[0].rstrip('{').strip()

            imports_add = ''
            if element_name in ('Window',
                    'ScrollView', 'Layout', 'ColumnLayout', 'RowLayout'):
                imports_add = 'import QtQuick.Layouts\n'

            for flip in (
                    ('CloseButton', 'ToolButton'),
                    ('MaxButton', 'ToolButton'),
                    ('MinButton', 'ToolButton')):
                theme = theme.replace(flip[0] + ' {', flip[1] + ' {')

            element_theme = imports.lstrip() + imports_add + theme
            element_theme_path = self.__qml_path / (element_name + '.qml')

            element_theme_path.write_text(element_theme)
