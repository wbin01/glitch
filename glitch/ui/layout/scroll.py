#!/usr/bin/env python3
from ..base import Layout


qml = """
ScrollView {
    id: scroll  // ID
    objectName: "scroll"  // Object name
    property string qmlType: "Scroll"  // Class Name
    property string baseClass: "Layout"  // Base class name

    Layout.fillWidth: true
    Layout.fillHeight: true
    clip: true
    contentWidth: availableWidth

    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin
    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0

    background: Rectangle {
        color: "#22000000"
        radius: 4
    }

    ColumnLayout {
        id: scrollColumn
        objectName: "scrollColumn"

        // width: parent.width
        // Layout.fillWidth: true
        width: parent.width
        spacing: 6

// Close
    }

}
"""
# Python set 
# scroll_view.setProperty("Layout.minimumHeight", 200)
# scroll_view.setProperty("Layout.maximumHeight", 200)


class Scroll(Layout):
    """Scrollable column layout object.

    It is a type like `Column` object, but scrollable.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = qml
        self._name = 'Scroll'

    def __str__(self) -> str:
        return "<class 'Scroll'>"
