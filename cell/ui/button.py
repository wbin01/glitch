#/usr/bin/env python3
import pathlib

from .element import Element

qml_code = """

Button {
    id: button
    objectName: "button"
    property string qmlType: "Button"
    property color borderColor: "#555"
    property color backgroundColor: "#444"
    property alias iconSource: icon.source
    property bool isHovered: false
    property bool hasIcon: iconSource !== ""

    Layout.preferredHeight: 30
    Layout.fillWidth: true
    Layout.fillHeight: false

    contentItem: Item {
        anchors.fill: parent

        Row {
            id: row
            spacing: 8
            anchors.centerIn: parent

            Image {
                id: icon
                objectName: "icon"
                source: ""
                visible: icon.source !== ""
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
            }

            Text {
                id: text
                objectName: "text"
                text: button.text
                color: "#ccc"
                verticalAlignment: Text.AlignVCenter
            }
        }
    }

    background: Rectangle {
        id: buttonBackground
        objectName: "buttonBackground"
        color: "#444"

        property color borderColor: "#444"
        border.color: background.borderColor

        border.width: 1
        radius: 6
    }

}

"""
class Button(Element):
    """..."""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text

        path = pathlib.Path(__file__).parent.parent
        self.__icon = path/'static'/'icons'/f'{icon}.svg'

        self.class_name = 'Button'
        self.qml = self.qml.replace(
            '\n// <property>',
            f'\n    text: "{self.__text}"'
            f'\n    iconSource: "{self.__icon}"'
            '\n// <property>')
