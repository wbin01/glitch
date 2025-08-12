#!/usr/bin/env python3
from ..base import Layout


header = """
ScrollView {
    id: scroll  // ID
    objectName: "scroll"  // Object name
    property string className: "Scroll"  // Class name
    property string baseClass: "Layout"  // Base class
    property string styleClass: "Scroll"  // Style class
    property string baseStyle: "Scroll"  // Base style
"""

properties = """
    Layout.fillWidth: true
    Layout.fillHeight: true

    clip: true
    contentWidth: availableWidth

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
"""
# } close on UI. Add // Property for inheritance


class Scroll(Layout):
    """Scrollable column layout object.

    It is a type like `Column` object, but scrollable.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._qml = header + self._qml.split('// Layout header')[1].replace(
            '// Close', '').replace('\n    // Property', properties)
        self.class_id('Scroll')

    def __str__(self) -> str:
        return "<class 'Scroll'>"
