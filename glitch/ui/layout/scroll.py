#!/usr/bin/env python3
from ..base import Box


header = """
ScrollView {
    id: scroll  // ID
    objectName: "scroll"  // Object name
    property string qmlType: "Scroll"  // Class Name
    property string baseClass: "Layout"  // Base class name
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


class Scroll(Box):
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
