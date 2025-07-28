#/usr/bin/env python3
from .base import Layout

object_code = """
// ScrollBox
ScrollView {
    Layout.fillWidth: true
    Layout.fillHeight: true
    clip: true
    contentWidth: availableWidth

    background: Rectangle {
        color: "#22000000"
        radius: 4
    }

    ColumnLayout {
        id: scrollBox
        objectName: "scrollBox"
        property string qmlType: "ScrollBox"
        // width: parent.width
        // Layout.fillWidth: true
        width: parent.width
        spacing: 10

// **closing_key**
    }

}  // ScrollBox id: scrollBox
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
        self._qml = object_code
        self.id = 'scrollBox'
