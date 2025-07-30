#/usr/bin/env python3
from ..base import Layout

object_code = """
// ScrollBox
ScrollView {
    id: scroll  // <id>
    objectName: "scroll"  // <objectName>
    property string qmlType: "Scroll"  // <className>

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
        id: scrollColumnLayout
        objectName: "scrollColumnLayout"

        // width: parent.width
        // Layout.fillWidth: true
        width: parent.width

        
        
        spacing: 6

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
        self._element_type = 'Scroll'

    def __str__(self):
        return f'<Scroll: {id(self)}>'
