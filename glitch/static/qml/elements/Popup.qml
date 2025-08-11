import QtQuick
import QtQuick.Controls
import QtQuick.Layouts


Popup {
    id: panel  // ID
    objectName: "panel"  // Object name
    property string className: "Panel"  // Class name
    property string baseClass: "Layout"  // Base class

    Canvas {
        id: canvas
        objectName: "canvas"
    }
}
