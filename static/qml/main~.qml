
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Shapes

import "elements"


Window {
    id: _134459965084432  // ID
    objectName: "_134459965084432"  // Object name
    property string className: "MainFrame"  // Class name
    property string baseClass: "Layout"  // Base class
    property string styleClass: "Frame"  // Style class
    property string baseStyle: "Frame"  // Base style


    // Layout header

    title: qsTr("Cell")
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
        id: mainRect
        objectName: "mainRect"
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

                // Função para desenhar retângulo arredondado com raios individuais
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
                roundedRect(1, 1, width - 2, height - 2,
                            mainRect.radiusTopLeft, mainRect.radiusTopRight,
                            mainRect.radiusBottomRight, mainRect.radiusBottomLeft);
                ctx.fillStyle = mainRect.backgroundColor;
                ctx.fill();

                // --- Outer border ---
                roundedRect(0, 0, width, height,
                            mainRect.radiusTopLeft + 2, mainRect.radiusTopRight + 2,
                            mainRect.radiusBottomRight + 2, mainRect.radiusBottomLeft + 2);
                ctx.strokeStyle = mainRect.outLineColor;
                ctx.lineWidth = mainRect.outLineWidth;
                ctx.stroke();

                // --- Inner border ---
                var inset = borderSpacing + mainRect.borderWidth / 2;
                roundedRect(
                    inset, inset,
                    width - inset * 2,
                    height - inset * 2,
                    Math.max(0, mainRect.radiusTopLeft - inset),
                    Math.max(0, mainRect.radiusTopRight - inset),
                    Math.max(0, mainRect.radiusBottomRight - inset),
                    Math.max(0, mainRect.radiusBottomLeft - inset)
                );
                ctx.strokeStyle = mainRect.borderColor;
                ctx.lineWidth = mainRect.borderWidth;
                ctx.stroke();
            }
        }


// MainFrame
        // Drag area
        Rectangle {
            id: dragArea
            objectName: "dragArea"
            // width: parent.width
            // width: parent.width - 20
            height: 20
            anchors {
                top: parent.top
                left: parent.left
                right: parent.right
                margins: 5  // margem de 10px nas laterais
            }
            color: "transparent"
            z: 0  // 2

            MouseArea {
                anchors.fill: parent
                drag.target: mainRect
                onPressed: logic.start_move()
            }
        }
// MainFrame


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
            // anchors.top: parent.top
            anchors.margins: 4
            spacing: 6
            clip: true
            // Layout.fillHeight: false
            Layout.alignment: Qt.AlignTop
            Layout.fillWidth: false

            RowLayout {
                id: _134459844669952  // ID
                objectName: "_134459844669952"  // Object name
                property string className: "Row"  // Class name
                property string baseClass: "UI"  // Base class name
                property string styleClass: "Row"  // Style class
                property string baseStyle: "Row"  // Base style


                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                // Layout header

                // Property

                Button {
                    id: action_close  // ID
                    objectName: "action_close"  // Object name
                    property string className: "FrameCloseButton"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "FrameCloseButton"  // Style class
                    property string baseStyle: "Button"  // Base style

                    height: 22
                    width: 22

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: false
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: ""
                    text: ""
                    checkable: false
                    checked: false


                }

                Button {
                    id: action_max  // ID
                    objectName: "action_max"  // Object name
                    property string className: "FrameMaxButton"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Button"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 22
                    width: 22

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: false
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: ""
                    text: ""
                    checkable: false
                    checked: false


                }

                Button {
                    id: action_min  // ID
                    objectName: "action_min"  // Object name
                    property string className: "FrameMinButton"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "FrameMinButton"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 22
                    width: 22

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: false
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: ""
                    text: ""
                    checkable: false
                    checked: false


                }

            
            }
            
    Popup {
        id: _134459846113520  // ID
        objectName: "_134459846113520"  // Object name
        property string className: "Panel"  // Class name
        property string baseClass: "Layout"  // Base class
        property string styleClass: "Panel"  // Style class
        property string baseStyle: "Panel"  // Base style


        padding: 1 // Frame border
        width: 250

        // Padding is 6 -> 6+6=12 -> 12-2 (2 is 1 pixel border on top and bottom) =10
        height: parent.height + 6  // 10

        x: 0

        // Half of the Frame padding - outer border
        y: - 3  // 5
        
        modal: false
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        clip: true

        transformOrigin: Item.Left

        property int parentHeight: parent.height + 6 // 10
        property int parentWidth: parent.width + 7 // 9  // 10 -1 detach from the right

        property color backgroundColor: "#222"
        property color borderColor: "#222"
        property int borderWidth: 1

        property int radiusTopLeft: 6
        property int radiusTopRight: 0
        property int radiusBottomRight: 0
        property int radiusBottomLeft: 0

        background: Rectangle {
            color: "#00000000"
            radius: 0
            border.color: "#00000000"
            border.width: 1
            clip: true
        }

        Canvas {
            id: canvas_134459846113520
            objectName: "canvas_134459846113520"
            anchors.fill: parent

            onPaint: {
                var ctx = getContext("2d");
                ctx.clearRect(0, 0, width, height);

                ctx.beginPath();
                ctx.moveTo(_134459846113520.radiusTopLeft, 0);
                ctx.lineTo(width - _134459846113520.radiusTopRight, 0);
                ctx.arcTo(width, 0, width, _134459846113520.radiusTopRight, _134459846113520.radiusTopRight);
                ctx.lineTo(width, height - _134459846113520.radiusBottomRight);
                ctx.arcTo(width, height, width - _134459846113520.radiusBottomRight, height, _134459846113520.radiusBottomRight);
                ctx.lineTo(_134459846113520.radiusBottomLeft, height);
                ctx.arcTo(0, height, 0, height - _134459846113520.radiusBottomLeft, _134459846113520.radiusBottomLeft);
                ctx.lineTo(0, _134459846113520.radiusTopLeft);
                ctx.arcTo(0, 0, _134459846113520.radiusTopLeft, 0, _134459846113520.radiusTopLeft);
                ctx.closePath();

                // Background color
                ctx.fillStyle = _134459846113520.backgroundColor;
                ctx.fill();

                // Border coloe
                ctx.strokeStyle = _134459846113520.borderColor;
                ctx.lineWidth = _134459846113520.borderWidth;
                ctx.stroke();
            }
        }

        ColumnLayout {
            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin
            spacing: 6
            anchors.fill: parent

        }
    
    
    
    
    }
    
    Popup {
        id: _134459844667648  // ID
        objectName: "_134459844667648"  // Object name
        property string className: "Panel"  // Class name
        property string baseClass: "Layout"  // Base class
        property string styleClass: "Panel"  // Style class
        property string baseStyle: "Panel"  // Base style


        padding: 1 // Frame border
        width: 250

        // Padding is 6 -> 6+6=12 -> 12-2 (2 is 1 pixel border on top and bottom) =10
        height: parent.height + 6  // 10

        x: 0

        // Half of the Frame padding - outer border
        y: - 3  // 5
        
        modal: false
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
        clip: true

        transformOrigin: Item.Right

        property int parentHeight: parent.height + 6 // 10
        property int parentWidth: parent.width + 7 // 9  // 10 -1 detach from the right

        property color backgroundColor: "#222"
        property color borderColor: "#222"
        property int borderWidth: 1

        property int radiusTopLeft: 0
        property int radiusTopRight: 6
        property int radiusBottomRight: 0
        property int radiusBottomLeft: 0

        background: Rectangle {
            color: "#00000000"
            radius: 0
            border.color: "#00000000"
            border.width: 1
            clip: true
        }

        Canvas {
            id: canvas_134459844667648
            objectName: "canvas_134459844667648"
            anchors.fill: parent

            onPaint: {
                var ctx = getContext("2d");
                ctx.clearRect(0, 0, width, height);

                ctx.beginPath();
                ctx.moveTo(_134459844667648.radiusTopLeft, 0);
                ctx.lineTo(width - _134459844667648.radiusTopRight, 0);
                ctx.arcTo(width, 0, width, _134459844667648.radiusTopRight, _134459844667648.radiusTopRight);
                ctx.lineTo(width, height - _134459844667648.radiusBottomRight);
                ctx.arcTo(width, height, width - _134459844667648.radiusBottomRight, height, _134459844667648.radiusBottomRight);
                ctx.lineTo(_134459844667648.radiusBottomLeft, height);
                ctx.arcTo(0, height, 0, height - _134459844667648.radiusBottomLeft, _134459844667648.radiusBottomLeft);
                ctx.lineTo(0, _134459844667648.radiusTopLeft);
                ctx.arcTo(0, 0, _134459844667648.radiusTopLeft, 0, _134459844667648.radiusTopLeft);
                ctx.closePath();

                // Background color
                ctx.fillStyle = _134459844667648.backgroundColor;
                ctx.fill();

                // Border coloe
                ctx.strokeStyle = _134459844667648.borderColor;
                ctx.lineWidth = _134459844667648.borderWidth;
                ctx.stroke();
            }
        }

        ColumnLayout {
            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin
            spacing: 6
            anchors.fill: parent

        ColumnLayout {
            id: _134459844667504  // ID
            objectName: "_134459844667504"  // Object name
            property string className: "Column"  // Class name
            property string baseClass: "UI"  // Base class name
            property string styleClass: "Column"  // Style class
            property string baseStyle: "Column"  // Base style


            property int topMargin: 10
            property int rightMargin: 10
            property int bottomMargin: 10
            property int leftMargin: 10
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            // Layout header

            // Property

            Button {
                id: panel_button  // ID
                objectName: "panel_button"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Hello"
                checkable: false
                checked: false


            }

        
        }
        
        }
    
    
    
    
    }
    
    Label {
        id: label  // ID
        objectName: "label"  // Object name
        property string className: "Label"  // Class name
        property string baseClass: "Element"  // Base class
        property string styleClass: "Label"  // Style class
        property string baseStyle: "Label"  // Base style


        height: 20
        width: 100

        property int alignment: Qt.AlignHCenter
        Layout.alignment: alignment

        property bool fillWidth: true
        property bool fillHeight: false
        Layout.fillWidth: fillWidth
        Layout.fillHeight: fillHeight
        
        Layout.preferredWidth: width
        Layout.preferredHeight: height

        // Layout header

        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 100
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin

        // Frame header

        text: "Panel slides from left"
        color: "#fff"

        // Layout.fillWidth: true
        // Layout.preferredHeight: 80
        // horizontalAlignment: Text.AlignHCenter
        // verticalAlignment: Text.AlignVCenter

    }

    Button {
        id: tool_button  // ID
        objectName: "tool_button"  // Object name
        property string className: "ToolButton"  // Class name
        property string baseClass: "Element"  // Base class
        property string styleClass: "Button"  // Style class
        property string baseStyle: "Button"  // Base style


        height: 30
        width: 30

        property int alignment: Qt.AlignHCenter
        Layout.alignment: alignment

        property bool fillWidth: false
        property bool fillHeight: false
        Layout.fillWidth: fillWidth
        Layout.fillHeight: fillHeight
        
        Layout.preferredWidth: width
        Layout.preferredHeight: height

        // Layout header

        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 0
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin

        // Frame header

        iconSource: "/usr/share/icons/breeze-dark/actions/22/document-save.svg"
        text: ""
        checkable: true
        checked: false


    }

    Button {
        id: button  // ID
        objectName: "button"  // Object name
        property string className: "Button"  // Class name
        property string baseClass: "Element"  // Base class
        property string styleClass: "Button"  // Style class
        property string baseStyle: "Button"  // Base style


        height: 50
        width: 100

        property int alignment: Qt.AlignHCenter
        Layout.alignment: alignment

        property bool fillWidth: true
        property bool fillHeight: false
        Layout.fillWidth: fillWidth
        Layout.fillHeight: fillHeight
        
        Layout.preferredWidth: width
        Layout.preferredHeight: height

        // Layout header

        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 0
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin

        // Frame header

        iconSource: "/usr/share/icons/breeze-dark/actions/16/document-open.svg"
        text: "Button check"
        checkable: true
        checked: false


    }

    ScrollView {
        id: _134459844125824  // ID
        objectName: "_134459844125824"  // Object name
        property string className: "Scroll"  // Class name
        property string baseClass: "Layout"  // Base class
        property string styleClass: "Scroll"  // Style class
        property string baseStyle: "Scroll"  // Base style


        property int topMargin: 10
        property int rightMargin: 10
        property int bottomMargin: 10
        property int leftMargin: 10
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin
        
        Layout.fillWidth: true
        Layout.fillHeight: true

        clip: true
        contentWidth: availableWidth

        background: Rectangle {
            color: "#1E000000"
            radius: 4
        }

        ColumnLayout {
            id: scrollColumn
            objectName: "scrollColumn"

            // width: parent.width
            // Layout.fillWidth: true
            width: parent.width
            spacing: 6

        ColumnLayout {
            id: _134459842428704  // ID
            objectName: "_134459842428704"  // Object name
            property string className: "Column"  // Class name
            property string baseClass: "UI"  // Base class name
            property string styleClass: "Column"  // Style class
            property string baseStyle: "Column"  // Base style


            property int topMargin: 10
            property int rightMargin: 10
            property int bottomMargin: 10
            property int leftMargin: 10
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            // Layout header

            // Property

            Button {
                id: button_0  // ID
                objectName: "button_0"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Button 0"
                checkable: false
                checked: false


            }

            Button {
                id: button_1  // ID
                objectName: "button_1"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Button 1"
                checkable: false
                checked: false


            }

            Button {
                id: _134459843726944  // ID
                objectName: "_134459843726944"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Button 2"
                checkable: false
                checked: false


            }

            Button {
                id: button_3  // ID
                objectName: "button_3"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Button 3"
                checkable: false
                checked: false


            }

            Button {
                id: button_4  // ID
                objectName: "button_4"  // Object name
                property string className: "Button"  // Class name
                property string baseClass: "Element"  // Base class
                property string styleClass: "Button"  // Style class
                property string baseStyle: "Button"  // Base style


                height: 30
                width: 100

                property int alignment: Qt.AlignHCenter
                Layout.alignment: alignment

                property bool fillWidth: true
                property bool fillHeight: false
                Layout.fillWidth: fillWidth
                Layout.fillHeight: fillHeight
                
                Layout.preferredWidth: width
                Layout.preferredHeight: height

                // Layout header

                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                iconSource: ""
                text: "Button 4"
                checkable: false
                checked: false


            }

            RowLayout {
                id: _134459842428608  // ID
                objectName: "_134459842428608"  // Object name
                property string className: "CustomElement"  // Class name
                property string baseClass: "UI"  // Base class name
                property string styleClass: "Row"  // Style class
                property string baseStyle: "Row"  // Base style


                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                // Layout header

                // Property

                Button {
                    id: _134459844838896  // ID
                    objectName: "_134459844838896"  // Object name
                    property string className: "Button"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Button"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 30
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: "/home/user/Dev/github/glitch/glitch/static/icons/linux/document-open.svg"
                    text: "Elves"
                    checkable: false
                    checked: false


                }

                Label {
                    id: _134459842412768  // ID
                    objectName: "_134459842412768"  // Object name
                    property string className: "Label"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Label"  // Style class
                    property string baseStyle: "Label"  // Base style


                    height: 20
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    text: "Label"
                    color: "#fff"

                    // Layout.fillWidth: true
                    // Layout.preferredHeight: 80
                    // horizontalAlignment: Text.AlignHCenter
                    // verticalAlignment: Text.AlignVCenter

                }

            
            }
            
            RowLayout {
                id: _134459842413104  // ID
                objectName: "_134459842413104"  // Object name
                property string className: "CustomElement"  // Class name
                property string baseClass: "UI"  // Base class name
                property string styleClass: "Row"  // Style class
                property string baseStyle: "Row"  // Base style


                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                // Layout header

                // Property

                Button {
                    id: _134459842413200  // ID
                    objectName: "_134459842413200"  // Object name
                    property string className: "Button"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Button"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 30
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: ""
                    text: "Button XX"
                    checkable: false
                    checked: false


                }

                Label {
                    id: _134459842413632  // ID
                    objectName: "_134459842413632"  // Object name
                    property string className: "Label"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Label"  // Style class
                    property string baseStyle: "Label"  // Base style


                    height: 20
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    text: "Label"
                    color: "#fff"

                    // Layout.fillWidth: true
                    // Layout.preferredHeight: 80
                    // horizontalAlignment: Text.AlignHCenter
                    // verticalAlignment: Text.AlignVCenter

                }

            
            }
            
            RowLayout {
                id: _134459842413968  // ID
                objectName: "_134459842413968"  // Object name
                property string className: "CustomElement"  // Class name
                property string baseClass: "UI"  // Base class name
                property string styleClass: "Row"  // Style class
                property string baseStyle: "Row"  // Base style


                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                // Layout header

                // Property

                Button {
                    id: _134459842414064  // ID
                    objectName: "_134459842414064"  // Object name
                    property string className: "Button"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Button"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 30
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: ""
                    text: "Button XX"
                    checkable: false
                    checked: false


                }

                Label {
                    id: _134459842414496  // ID
                    objectName: "_134459842414496"  // Object name
                    property string className: "Label"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Label"  // Style class
                    property string baseStyle: "Label"  // Base style


                    height: 20
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    text: "Label"
                    color: "#fff"

                    // Layout.fillWidth: true
                    // Layout.preferredHeight: 80
                    // horizontalAlignment: Text.AlignHCenter
                    // verticalAlignment: Text.AlignVCenter

                }

            
            }
            
            RowLayout {
                id: _134459842414832  // ID
                objectName: "_134459842414832"  // Object name
                property string className: "CustomElement"  // Class name
                property string baseClass: "UI"  // Base class name
                property string styleClass: "Row"  // Style class
                property string baseStyle: "Row"  // Base style


                property int topMargin: 0
                property int rightMargin: 0
                property int bottomMargin: 0
                property int leftMargin: 0
                Layout.topMargin: topMargin
                Layout.rightMargin: rightMargin
                Layout.bottomMargin: bottomMargin
                Layout.leftMargin: leftMargin

                // Frame header

                // Layout header

                // Property

                Button {
                    id: _134459842415072  // ID
                    objectName: "_134459842415072"  // Object name
                    property string className: "Button"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Button"  // Style class
                    property string baseStyle: "Button"  // Base style


                    height: 30
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    iconSource: "/home/user/Dev/github/glitch/glitch/static/icons/linux/document-open.svg"
                    text: "Elves"
                    checkable: false
                    checked: false


                }

                Label {
                    id: _134459842415456  // ID
                    objectName: "_134459842415456"  // Object name
                    property string className: "Label"  // Class name
                    property string baseClass: "Element"  // Base class
                    property string styleClass: "Label"  // Style class
                    property string baseStyle: "Label"  // Base style


                    height: 20
                    width: 100

                    property int alignment: Qt.AlignHCenter
                    Layout.alignment: alignment

                    property bool fillWidth: true
                    property bool fillHeight: false
                    Layout.fillWidth: fillWidth
                    Layout.fillHeight: fillHeight
                    
                    Layout.preferredWidth: width
                    Layout.preferredHeight: height

                    // Layout header

                    property int topMargin: 0
                    property int rightMargin: 0
                    property int bottomMargin: 0
                    property int leftMargin: 0
                    Layout.topMargin: topMargin
                    Layout.rightMargin: rightMargin
                    Layout.bottomMargin: bottomMargin
                    Layout.leftMargin: leftMargin

                    // Frame header

                    text: "Label"
                    color: "#fff"

                    // Layout.fillWidth: true
                    // Layout.preferredHeight: 80
                    // horizontalAlignment: Text.AlignHCenter
                    // verticalAlignment: Text.AlignVCenter

                }

            
            }
            
        
        }
        
        }
    
    
    
    
    }
    
    RowLayout {
        id: _134459842415696  // ID
        objectName: "_134459842415696"  // Object name
        property string className: "Row"  // Class name
        property string baseClass: "UI"  // Base class name
        property string styleClass: "Row"  // Style class
        property string baseStyle: "Row"  // Base style


        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 0
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin

        // Frame header

        // Layout header

        // Property

        Button {
            id: _134459842415936  // ID
            objectName: "_134459842415936"  // Object name
            property string className: "Button"  // Class name
            property string baseClass: "Element"  // Base class
            property string styleClass: "Button"  // Style class
            property string baseStyle: "Button"  // Base style


            height: 30
            width: 100

            property int alignment: Qt.AlignHCenter
            Layout.alignment: alignment

            property bool fillWidth: true
            property bool fillHeight: false
            Layout.fillWidth: fillWidth
            Layout.fillHeight: fillHeight
            
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            // Layout header

            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            iconSource: ""
            text: "Ok"
            checkable: false
            checked: false


        }

        Button {
            id: _134459844025696  // ID
            objectName: "_134459844025696"  // Object name
            property string className: "Button"  // Class name
            property string baseClass: "Element"  // Base class
            property string styleClass: "Button"  // Style class
            property string baseStyle: "Button"  // Base style


            height: 30
            width: 100

            property int alignment: Qt.AlignHCenter
            Layout.alignment: alignment

            property bool fillWidth: true
            property bool fillHeight: false
            Layout.fillWidth: fillWidth
            Layout.fillHeight: fillHeight
            
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            // Layout header

            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            iconSource: ""
            text: "Cancel"
            checkable: false
            checked: false


        }

    
    }
    
    ColumnLayout {
        id: _134459846108864  // ID
        objectName: "_134459846108864"  // Object name
        property string className: "Column"  // Class name
        property string baseClass: "UI"  // Base class name
        property string styleClass: "Column"  // Style class
        property string baseStyle: "Column"  // Base style


        property int topMargin: 0
        property int rightMargin: 0
        property int bottomMargin: 0
        property int leftMargin: 0
        Layout.topMargin: topMargin
        Layout.rightMargin: rightMargin
        Layout.bottomMargin: bottomMargin
        Layout.leftMargin: leftMargin

        // Frame header

        // Layout header

        // Property

        Button {
            id: _134459838999120  // ID
            objectName: "_134459838999120"  // Object name
            property string className: "Button"  // Class name
            property string baseClass: "Element"  // Base class
            property string styleClass: "Button"  // Style class
            property string baseStyle: "Button"  // Base style


            height: 30
            width: 100

            property int alignment: Qt.AlignHCenter
            Layout.alignment: alignment

            property bool fillWidth: true
            property bool fillHeight: false
            Layout.fillWidth: fillWidth
            Layout.fillHeight: fillHeight
            
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            // Layout header

            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            iconSource: ""
            text: "Button 1"
            checkable: false
            checked: false


        }

        Button {
            id: button_2  // ID
            objectName: "button_2"  // Object name
            property string className: "Button"  // Class name
            property string baseClass: "Element"  // Base class
            property string styleClass: "button_2"  // Style class
            property string baseStyle: "Button"  // Base style


            height: 30
            width: 100

            property int alignment: Qt.AlignHCenter
            Layout.alignment: alignment

            property bool fillWidth: true
            property bool fillHeight: false
            Layout.fillWidth: fillWidth
            Layout.fillHeight: fillHeight
            
            Layout.preferredWidth: width
            Layout.preferredHeight: height

            // Layout header

            property int topMargin: 0
            property int rightMargin: 0
            property int bottomMargin: 0
            property int leftMargin: 0
            Layout.topMargin: topMargin
            Layout.rightMargin: rightMargin
            Layout.bottomMargin: bottomMargin
            Layout.leftMargin: leftMargin

            // Frame header

            iconSource: ""
            text: "Button 2"
            checkable: false
            checked: false


        }

    
    }
    

        }
    }




}
