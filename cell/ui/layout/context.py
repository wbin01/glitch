#!/usr/bin/env python3
from ..base import Layout


qml_popup = """
Popup {
    id: context  // <id>
    objectName: "context"  // <objectName>
    property string qmlType: "Context"  // <className>
    property string baseClass: "Frame"  // <baseClass>

    width: 250
    height: parent.height - 40
    x: parent.width - width - 20
    y: 20
    modal: false
    closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside

    background: Rectangle {
        color: "#2c2c2c"
        radius: 12
        border.color: "#555"
        border.width: 2
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

qml_drawer = """
Drawer {
    id: context  // <id>
    objectName: "context"  // <objectName>
    property string qmlType: "Context"  // <className>
    property string baseClass: "Frame"  // <baseClass>

    edge: Qt.LeftEdge
    width: parent.width * 0.6
    height: parent.height

    background: Rectangle {
        color: "#1e1e1e"
        radius: 0
        border.color: "#666"
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


class Context(Layout):
    """Context layout.

    Can behave as a panel or a frame. Setting the panel parameter to true will 
    make this context behave as a panel; otherwise, it will adapt as a 
    floating frame.
    """
    def __init__(self, panel: bool = True, *args, **kwargs) -> None:
        """
        :param panel: Use `True` for the context to always behave like a panel.
        """
        super().__init__(resizable=True, *args, **kwargs)
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
