import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id: panel  // <id>
    objectName: "panel"  // <objectName>
    property string qmlType: "Panel"  // <className>
    property string baseClass: "Layout"  // <baseClass>

    padding: 0
    width: 250
    height: parent.height + 10 // Frame padding
    x: - 5 // Half of the Frame padding
    y: - 5
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    clip: true

    transformOrigin: Item.Left

    property color backgroundColor: "#222"
    property color borderColor: "#222"
    property int borderWidth: 1

    background: Rectangle {
        color: "#00000000"
        radius: 0
        border.color: "#00000000"
        border.width: 1
        clip: true
    }

    Canvas {
        id: canvas
        objectName: "canvas"
        anchors.fill: parent

        // Connections {
        //     target: panel
        //     function onBackgroundColorChanged() { canv.requestPaint() }
        //     function onBorderColorChanged() { canv.requestPaint() }
        //     function onBorderWidthChanged() { canv.requestPaint() }
        // }

        onPaint: {
            var ctx = getContext("2d");
            ctx.clearRect(0, 0, width, height);

            var radiusTopLeft = 10;
            var radiusTopRight = 0;
            var radiusBottomRight = 0;
            var radiusBottomLeft = 10;

            ctx.beginPath();
            ctx.moveTo(radiusTopLeft, 0);
            ctx.lineTo(width - radiusTopRight, 0);
            ctx.arcTo(width, 0, width, radiusTopRight, radiusTopRight);
            ctx.lineTo(width, height - radiusBottomRight);
            ctx.arcTo(width, height, width - radiusBottomRight, height, radiusBottomRight);
            ctx.lineTo(radiusBottomLeft, height);
            ctx.arcTo(0, height, 0, height - radiusBottomLeft, radiusBottomLeft);
            ctx.lineTo(0, radiusTopLeft);
            ctx.arcTo(0, 0, radiusTopLeft, 0, radiusTopLeft);
            ctx.closePath();

            // Background color
            ctx.fillStyle = panel.backgroundColor;
            ctx.fill();

            // Border coloe
            ctx.strokeStyle = panel.borderColor;
            ctx.lineWidth = panel.borderWidth;
            ctx.stroke();
        }
    }
}