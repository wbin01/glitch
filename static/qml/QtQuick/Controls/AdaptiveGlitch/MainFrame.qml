import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts

Window {
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

        property color backgroundColor: "#ff323232"
        property color borderColor: "#ff414141"
        property color outLineColor: "#44000000"
        property int borderWidth: 1
        property int outLineWidth: 1

        property int radiusTopLeft: 8
        property int radiusTopRight: 8
        property int radiusBottomRight: 8
        property int radiusBottomLeft: 8

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