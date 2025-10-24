#!/usr/bin/env python3
from ..ui import UI


qml_header = """
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

"""

window_properties = """
    title: qsTr("UI")
    color: "transparent"
    flags: Qt.FramelessWindowHint

    width: 400
    height: 400

    minimumWidth: 100
    minimumHeight: 30

    visible: true
    visibility: Window.Windowed

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

        property color backgroundColor: "#222"
        property color borderColor: "#333"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: 6
        property int radiusTopRight: 6
        property int radiusBottomRight: 0
        property int radiusBottomLeft: 0

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
            Layout.fillWidth: false
    // } }
"""

class QmlBuilder(object):
    """..."""
    def __init__(self, ui: UI) -> None:
        """
        :param ui:
        """
        self.__ui = ui
        self.__qml_code = ''
        self.__first_iteration = True
        self.__write_qml(self.__ui)
        self.__qml_finish()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(ui={self.__ui!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(ui={self.__ui!r})'

    @property
    def _qml(self) -> str:
        """..."""
        return self.__qml_code

    def __write_qml(self, ui: UI, tab: str = '') -> None:
        if not hasattr(ui, '_QtObject__items'):
            return

        # Main Layout ID
        if '// id' in ui.qml and self.__first_iteration:
            id_ = ui.__class__.__name__.lower()
            ui.qml = ui.qml.replace(
                '// id', f'id: {id_}').replace(
                '// objectName', f'objectName: "{id_}"').replace(
                '// Close ' + ui._name, '// Close ' + id_).replace(
                '// +', window_properties + '\n    // +\n')

        # UIs ID
        for name, value in ui.__dict__.items():
            element = getattr(ui, name)
            if isinstance(element, UI):
                id_ = name.lower()
                element.qml = element.qml.replace(
                    '// id', f'id: {id_}').replace(
                    '// objectName', f'objectName: "{id_}"\n').replace(
                    '// Close ' + element._name, '// Close ' + id_)

        # UIs headers and his properties
        header, body = ui.qml.split('// +')
        qml_end = body.strip('\n')
        if self.__first_iteration:
            qml_end = (
                '\n        } // Close mainColumnLayout'
                '\n    } // Close mainRectangle\n' + qml_end)

        for line in header.split('\n'):
            if '//' not in line:
                self.__qml_code += tab + line + '\n'
        self.__qml_code = self.__qml_code.strip() + '\n'

        # UI childs
        tab += '    '
        if self.__first_iteration:
            tab += '        '

        self.__first_iteration = False
        for element in ui._QtObject__items:
            element_items = (getattr(element, '_QtObject__items')
                if hasattr(element, '_QtObject__items') else None)
            
            if element_items and isinstance(element_items, list):
                self.__write_qml(element, tab)
            else:
                for qml_line in element.qml.split('\n'):
                    if '// Close' in qml_line:
                        qml_line = qml_line.split('// Close')[0].rstrip()
                    if qml_line and '//' not in qml_line:
                        self.__qml_code += tab + qml_line + '\n'
        # Close
        self.__qml_code = self.__qml_code + tab[:-4] + qml_end + '\n'

    def __qml_finish(self) -> None:
        sparse_qml = ''
        for line in self.__qml_code.split('\n'):
            if line.strip():
                if '{' in line:
                    sparse_qml += '\n' + line + '\n'
                elif '}' in line:
                    sparse_qml += line + '\n'
                else:
                    sparse_qml += line + '\n'
        self.__qml_code = qml_header + sparse_qml.replace('// Close ', '// ')
