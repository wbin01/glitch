#!/usr/bin/env python3


qml_style = """
import QtQuick
import QtQuick.Controls
// sep imports-elements
// +
BaseFrame {
    title: "Glitch App"
    color: "transparent"
    flags: Qt.FramelessWindowHint

    width: 200
    height: 30

    minimumWidth: 100
    minimumHeight: 30

    // visibility: Window.Windowed

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
        z: -1
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

        property color backgroundColor: "[Frame]background_color"
        property color borderColor: "[Frame]border_color"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: [Frame]border_radius_tl
        property int radiusTopRight: [Frame]border_radius_tr
        property int radiusBottomRight: [Frame]border_radius_br
        property int radiusBottomLeft: [Frame]border_radius_bl

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
MainFrame {
    id: win
    title: "Glitch App"
    color: "transparent"
    flags: Qt.FramelessWindowHint

    width: 400
    height: 400

    minimumWidth: 100
    minimumHeight: 30

    property bool movable: false
    property bool resizable: false

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
        z: -1
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
                    // 10, 10, width - 20, height - 20,
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
                // ctx.lineWidth = 20;
                ctx.lineWidth = mainRectangle.outLineWidth;
                ctx.stroke();

                // --- Inner border ---
                // var inset = borderSpacing + mainRectangle.borderWidth / 2 + 10;
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
                // drag.target: <id>
                // onPressed: logic.start_move()
                onPressed: {
                    if (win.movable) {
                        logic.start_move()
                    }
                }

                onDoubleClicked: {
                    if (win.resizable) {
                        logic.max_min()
                    }
                }
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
            // cursorShape: Qt.SizeFDiagCursor
            cursorShape: win.resizable ? Qt.SizeFDiagCursor : Qt.ArrowCursor
            // enabled: win.resizable
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.TopEdge | Qt.LeftEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.TopEdge | Qt.LeftEdge)
                }
            }
        }

        // Top right - resize NE
        MouseArea {
            id: resizeTopRight
            width: 10
            height: 10
            anchors.top: parent.top
            anchors.right: parent.right
            cursorShape: win.resizable ? Qt.SizeBDiagCursor : Qt.ArrowCursor
            hoverEnabled: true
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.TopEdge | Qt.RightEdge)
                }
            }
        }

        // Bottom left - resize SW
        MouseArea {
            id: resizeBottomLeft
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            cursorShape: win.resizable ? Qt.SizeBDiagCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.BottomEdge | Qt.LeftEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.BottomEdge | Qt.LeftEdge)
                }
            }
        }

        // Bottom right - resize SE
        MouseArea {
            id: resizeBottomRight
            width: 10
            height: 10
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            cursorShape: win.resizable ? Qt.SizeFDiagCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.BottomEdge | Qt.RightEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.BottomEdge | Qt.RightEdge)
                }
            }
        }

        // Top - N
        MouseArea {
            id: resizeTop
            anchors.top: parent.top
            anchors.left: resizeTopLeft.right
            anchors.right: resizeTopRight.left
            height: 5
            cursorShape: win.resizable ? Qt.SizeVerCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.TopEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.TopEdge)
                }
            }
        }

        // Bottom - S
        MouseArea {
            id: resizeBottom
            anchors.bottom: parent.bottom
            anchors.left: resizeBottomLeft.right
            anchors.right: resizeBottomRight.left
            height: 5
            cursorShape: win.resizable ? Qt.SizeVerCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.BottomEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.BottomEdge)
                }
            }
        }

        // Left - W
        MouseArea {
            id: resizeLeft
            anchors.top: resizeTopLeft.bottom
            anchors.bottom: resizeBottomLeft.top
            anchors.left: parent.left
            width: 5
            cursorShape: win.resizable ? Qt.SizeHorCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.LeftEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.LeftEdge)
                }
            }
        }

        // Right - E
        MouseArea {
            id: resizeRight
            anchors.top: resizeTopRight.bottom
            anchors.bottom: resizeBottomRight.top
            anchors.right: parent.right
            width: 5
            cursorShape: win.resizable ? Qt.SizeHorCursor : Qt.ArrowCursor
            hoverEnabled: true
            // onPressed: logic.start_resize(Qt.RightEdge)
            onPressed: {
                if (win.resizable) {
                    logic.start_resize(Qt.RightEdge)
                }
            }
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
Panel {
    id: panel
    width: 300
    x: 0
    y: 0
    // modal: true

    property color backgroundColor: "[Panel]background_color"
    property color borderColor: "[Panel]border_color"
    property color outLineColor: "#00000000"
    property int borderWidth: 1
    property int outLineWidth: 1

    property int radiusTopLeft: [Frame]border_radius_tl
    property int radiusTopRight: [Frame]border_radius_tr
    property int radiusBottomRight: [Frame]border_radius_br
    property int radiusBottomLeft: [Frame]border_radius_bl

    background: Item {
        id: bg
        anchors.fill: parent   // Isso é OK; background não é gerenciado por layouts

        Canvas {
            id: canvas
            objectName: "canvas"
            anchors.fill: parent
            // Layout.fillWidth: true
            // Layout.fillHeight: true
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
                    panel.radiusTopLeft,
                    panel.radiusTopRight,
                    panel.radiusBottomRight,
                    panel.radiusBottomLeft);

                ctx.fillStyle = panel.backgroundColor;
                ctx.fill();

                // --- Outer border ---
                roundedRect(
                    0, 0, width, height,
                    panel.radiusTopLeft + 2,
                    panel.radiusTopRight + 2,
                    panel.radiusBottomRight + 2,
                    panel.radiusBottomLeft + 2);

                ctx.strokeStyle = panel.outLineColor;
                ctx.lineWidth = panel.outLineWidth;
                ctx.stroke();

                // --- Inner border ---
                var inset = borderSpacing + panel.borderWidth / 2;
                roundedRect(
                    inset, inset,
                    width - inset * 2,
                    height - inset * 2,
                    Math.max(0, panel.radiusTopLeft - inset),
                    Math.max(0, panel.radiusTopRight - inset),
                    Math.max(0, panel.radiusBottomRight - inset),
                    Math.max(0, panel.radiusBottomLeft - inset));

                ctx.strokeStyle = panel.borderColor;
                ctx.lineWidth = panel.borderWidth;
                ctx.stroke();
            }
        }
    }

    contentItem: ColumnLayout {
        id: panelColumnLayout
        anchors.fill: parent
        spacing: 6
        anchors.margins: 0
    }

    default property alias content: panelColumnLayout.data
}

// +
ScrollView {
    id: scroll
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
    implicitHeight: 32

    icon.source: ""
    property alias iconSource: iconItem.source
    
    contentItem: Item {
        id: wrapper
        anchors.fill: parent

        Row {
            id: row
            spacing: button.icon.source !== "" ? 6 : 0
            anchors.centerIn: parent

            Image {
                id: iconItem
                source: button.icon.source
                width: button.icon.width
                height: visible ? button.icon.height : 0
                fillMode: Image.PreserveAspectFit
                visible: button.icon.source !== ""

                opacity: button.enabled ? 
                    [Button]icon_opacity : [Button:inactive]icon_opacity
            }

            Text {
                id: label
                text: button.text
                font: button.font
                verticalAlignment: Text.AlignVCenter

                color: !button.enabled ?
                    "[Button:inactive]font_color" : "[Button]font_color"
            }
        }
    }

    background: Rectangle {
        anchors.fill: parent

        color:
            !button.enabled && button.checked ?
                "[Button:checked:inactive]background_color" :
            !button.enabled ?
                "[Button:inactive]background_color" :

            button.checked && button.hovered ?
                "[Button:checked:hover]background_color" :
            button.checked ?
                "[Button:checked]background_color" :
            
            button.down ?
                "[Button:clicked]background_color" :
            button.hovered ?
                "[Button:hover]background_color" : "[Button]background_color"

        border.color:
            !button.enabled && button.checked ?
                "[Button:checked:inactive]border_color" :
            !button.enabled ?
                "[Button:inactive]border_color" :

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
    property url normalIcon: "[CloseButton]icon"
    property url hoverIcon: "[CloseButton:hover]icon"
    property url clickedIcon: "[CloseButton:clicked]icon"

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
                "[CloseButton:clicked]background_color" :
            appCloseButton.hovered ?
                "[CloseButton:hover]background_color" :
                "[CloseButton]background_color"

        border.color:
            appCloseButton.down ?
                "[CloseButton:clicked]border_color" :
            appCloseButton.hovered ?
                "[CloseButton:hover]border_color" :
                "[CloseButton]border_color"

        border.width: [CloseButton]border_width
        radius: [CloseButton]border_radius
    }
}
// +
FullButton {
    id: appFullButton
    padding: 0
    property url normalIcon: "[FullButton]icon"
    property url hoverIcon: "[FullButton:hover]icon"
    property url clickedIcon: "[FullButton:clicked]icon"

    property url restoreNormalIcon: "[FullButton]restore_icon"
    property url restoreHoverIcon: "[FullButton:hover]restore_icon"
    property url restoreClickedIcon: "[FullButton:clicked]restore_icon"

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
                "[FullButton:clicked]background_color" :
            appFullButton.hovered ?
                "[FullButton:hover]background_color" :
                "[FullButton]background_color"

        border.color:
            appFullButton.down ?
                "[FullButton:clicked]border_color" :
            appFullButton.hovered ?
                "[FullButton:hover]border_color" :
                "[FullButton]border_color"

        border.width: [FullButton]border_width
        radius: [FullButton]border_radius
    }
}
// +
MaxButton {
    id: appMaxButton
    padding: 0
    property url normalIcon: "[MaxButton]icon"
    property url hoverIcon: "[MaxButton:hover]icon"
    property url clickedIcon: "[MaxButton:clicked]icon"

    property url restoreNormalIcon: "[MaxButton]restore_icon"
    property url restoreHoverIcon: "[MaxButton:hover]restore_icon"
    property url restoreClickedIcon: "[MaxButton:clicked]restore_icon"

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
                "[MaxButton:clicked]background_color" :
            appMaxButton.hovered ?
                "[MaxButton:hover]background_color" :
                "[MaxButton]background_color"

        border.color:
            appMaxButton.down ?
                "[MaxButton:clicked]border_color" :
            appMaxButton.hovered ?
                "[MaxButton:hover]border_color" :
                "[MaxButton]border_color"

        border.width: [MaxButton]border_width
        radius: [MaxButton]border_radius
    }
}
// +
MinButton {
    id: appMinButton
    padding: 0
    property url normalIcon: "[MinButton]icon"
    property url hoverIcon: "[MinButton:hover]icon"
    property url clickedIcon: "[MinButton:clicked]icon"

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
                "[MinButton:clicked]background_color" :
            appMinButton.hovered ?
                "[MinButton:hover]background_color" :
                "[MinButton]background_color"

        border.color:
            appMinButton.down ?
                "[MinButton:clicked]border_color" :
            appMinButton.hovered ?
                "[MinButton:hover]border_color" :
                "[MinButton]border_color"

        border.width: [MinButton]border_width
        radius: [MinButton]border_radius
    }
}
// +
ToolButton {
    id: toolButton
    // implicitHeight: 32

    icon.source: ""
    property alias iconSource: iconItem.source
    
    contentItem: Image {
        id: iconItem
        anchors.centerIn: parent

        source: toolButton.icon.source
        width: toolButton.icon.width
        height: toolButton.icon.height
        fillMode: Image.PreserveAspectFit

        opacity: toolButton.enabled ? 
            [ToolButton]icon_opacity : [ToolButton:inactive]icon_opacity
    }

    background: Rectangle {
        anchors.fill: parent

        color:
            !toolButton.enabled && toolButton.checked ?
                "[ToolButton:checked:inactive]background_color" :
            !toolButton.enabled ?
                "[ToolButton:inactive]background_color" :

            toolButton.checked && toolButton.hovered ?
                "[ToolButton:checked:hover]background_color" :
            toolButton.checked ?
                "[ToolButton:checked]background_color" :
            
            toolButton.down ?
                "[ToolButton:clicked]background_color" :
            toolButton.hovered ?
                "[ToolButton:hover]background_color" : 
                "[ToolButton]background_color"

        border.color:
            !toolButton.enabled && toolButton.checked ?
                "[ToolButton:checked:inactive]border_color" :
            !toolButton.enabled ?
                "[ToolButton:inactive]border_color" :

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
    color:
        !label.enabled ? "[Label:inactive]font_color" : "[Label]font_color"
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
                if 'Frame' in style_header and key == 'border_radius':
                    for val, edge in zip(
                            value.split(','), ('_tl', '_tr', '_br', '_bl')):
                        self.__qml_style = self.__qml_style.replace(
                            mark + edge, val.strip())
                else:
                    self.__qml_style = self.__qml_style.replace(mark, value)

        imports, themes = self.__qml_style.split('// sep imports-elements')
        for theme in themes.split('// +'):
            if not theme.strip():
                continue

            element_name = theme.strip().split('\n')[0].rstrip('{').strip()

            imports_add = ''
            if element_name in (
                    'Window', 'BaseFrame', 'MainFrame', 'Panel',
                    'ScrollView', 'Layout', 'ColumnLayout', 'RowLayout'):
                imports_add = 'import QtQuick.Layouts\n'

            for flip in (
                    ('BaseFrame', 'Window'), ('MainFrame', 'Window'),
                    ('Panel', 'Popup'),
                    ('CloseButton', 'ToolButton'),
                    ('MaxButton', 'ToolButton'),
                    ('MinButton', 'ToolButton')):
                theme = theme.replace(flip[0] + ' {', flip[1] + ' {')

            element_theme = imports.lstrip() + imports_add + theme
            element_theme_path = self.__qml_path / (element_name + '.qml')

            element_theme_path.write_text(element_theme)
