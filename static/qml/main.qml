
import QtQuick
import QtQuick.Controls
// import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Layouts
import QtQuick.Shapes

Window {
    id: window
    objectName: "window"
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
                roundedRect(
                    1, 1, width - 2, height - 2,
                    mainRectangle.radiusTopLeft,
                    mainRectangle.radiusTopRight,
                    mainRectangle.radiusBottomRight,
                    mainRectangle.radiusBottomLeft);
                ctx.fillStyle = mainRectangle.backgroundColor;
                ctx.fill();
                roundedRect(
                    0, 0, width, height,
                    mainRectangle.radiusTopLeft + 2,
                    mainRectangle.radiusTopRight + 2,
                    mainRectangle.radiusBottomRight + 2,
                    mainRectangle.radiusBottomLeft + 2);
                ctx.strokeStyle = mainRectangle.outLineColor;
                ctx.lineWidth = mainRectangle.outLineWidth;
                ctx.stroke();
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

        Rectangle {
            id: dragArea
            objectName: "dragArea"
            height: 20

            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
            }
            color: "transparent"
            z: 0

            MouseArea {
                anchors.fill: parent
                onPressed: logic.start_move()
            }
        }

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

        ColumnLayout {
            id: mainColumnLayout
            objectName: "mainColumnLayout"
            anchors.fill: parent
            anchors.margins: 4
            spacing: 6
            clip: true
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: false

            Label {
                id: _window__label
                objectName: "_window__label"
                text: "Label xxx"
            }

            ColumnLayout {
                id: custom_col
                objectName: "custom_col"
                spacing: 6
                clip: true
                Layout.alignment: Qt.AlignTop
                Layout.fillWidth: false
                Layout.leftMargin: 15

                Button {
                    id: btn_top
                    objectName: "btn_top"
                    text: "TOOOp"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Label {
                    id: _window__label_custom_col
                    objectName: "_window__label_custom_col"
                    text: "Label custom col"
                }
            }  // custom_col

            Button {
                id: _window__custom_btn
                objectName: "_window__custom_btn"
                text: "CustomButton"
                icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
            }

            ColumnLayout {
                id: col
                objectName: "col"
                spacing: 6
                clip: true
                Layout.alignment: Qt.AlignTop
                Layout.fillWidth: false
                Layout.leftMargin: 15

                Button {
                    id: btn_click
                    objectName: "btn_click"
                    text: "Button 1"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: _window__btn2
                    objectName: "_window__btn2"
                    text: "Button 2"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: _window__btn3
                    objectName: "_window__btn3"
                    text: "Button 3"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: _window__btn4
                    objectName: "_window__btn4"
                    text: "Button 4"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: _window__btn5
                    objectName: "_window__btn5"
                    text: "Button 5"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: _window__btn6
                    objectName: "_window__btn6"
                    text: "Button 6"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: button0
                    objectName: "button0"
                    text: "Button range(0)"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }

                Button {
                    id: button1
                    objectName: "button1"
                    text: "Button range(1)"
                    icon.source: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
                }
            }  // col
        } // mainColumnLayout
    } // mainRectangle
}  // window
