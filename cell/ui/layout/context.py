#!/usr/bin/env python3
from ..base import Layout


qml_popup = """
Popup {
    id: context  // <id>
    objectName: "context"  // <objectName>
    property string qmlType: "Context"  // <className>
    property string baseClass: "Frame"  // <baseClass>

    width: 250
    height: parent.height + 10 // - 40
    x: - 5 // metade do padding da janela // parent.width - width // - 20
    y: - 5
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    clip: true

    background: Rectangle {
        color: "#2c2c2c"
        radius: 0
        border.color: "#555"
        border.width: 1
        clip: true
    }
    Behavior on x { NumberAnimation { duration: 250; easing.type: Easing.OutQuad } }

    ColumnLayout {
        id: column  // <id>
        objectName: "column"  // <objectName>
        property string qmlType: "Column"  // <className>
        property string baseClass: "Layout"  // <baseClass>
        
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
        // anchors.margins: 6

// **closing_key**
    }
}
"""

qml_drawer = """
Drawer {
    id: context  // <id>
    objectName: "context"  // <objectName>
    property string qmlType: "Context"  // <className>
    property string baseClass: "Frame"  // <baseClass>

    edge: Qt.LeftEdge
    width: parent.width * 0.4
    height: parent.height
    clip: true

    background: Rectangle {
        anchors.fill: parent
        anchors.margins: 0
        color: "#EF1A1A1A"
        radius: 0
        border.color: "#EF1A1A1A"
        border.width: 1
    }

    ColumnLayout {
        id: column  // <id>
        objectName: "column"  // <objectName>
        property string qmlType: "Column"  // <className>
        property string baseClass: "Layout"  // <baseClass>
        
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
        // anchors.margins: 6

// **closing_key**
    }
}
"""

# TESTS
# =====

qml_popup = """
Popup {
    id: context  // <id>
    objectName: "context"  // <objectName>
    property string qmlType: "Context"  // <className>
    property string baseClass: "Layout"  // <baseClass>

    padding: 0
    width: 250
    height: parent.height + 10 // + 10 do padding da janela
    x: - 5 // - metade do padding da janela
    y: - 5
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
    clip: true

    transformOrigin: Item.Left

    background: Rectangle {
        color: "#00000000"
        radius: 0
        border.color: "#00000000"
        border.width: 1
        clip: true
    }

    Canvas {
        id: canv
        anchors.fill: parent
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

            ctx.fillStyle = "#EF1A1A1A";
            ctx.fill();
        }
    }

    ColumnLayout {
        id: column  // <id>
        objectName: "column"  // <objectName>
        property string qmlType: "Column"  // <className>
        property string baseClass: "Layout"  // <baseClass>
        
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
        // anchors.margins: 6

// **closing_key**
    }
}
"""

class Context(Layout):
    """Context layout.

    Can behave as a panel or a frame. Setting the panel parameter to true will 
    make this context behave as a panel; otherwise, it will adapt as a 
    floating frame.
    """
    def __init__(self, panel: bool = False, *args, **kwargs) -> None:
        """
        :param panel: Use `True` for the context to always behave like a panel.
        """
        super().__init__(*args, **kwargs)
        self.__qml_drawer = qml_drawer
        self.__qml_popup = qml_popup

        self._qml = self.__qml_drawer if panel else self.__qml_popup
        self._element_type = 'Context'

    def open(self):
        """Open and display the context.

        By default, the context is not visible; this "open()" method is used 
        to display it.
        """
        if self._obj:
            self._obj.open()

    def __str__(self) -> str:
        return "<class 'Context'>"
