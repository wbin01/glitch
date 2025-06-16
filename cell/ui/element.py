#/usr/bin/env python3


qml_code = """
Element {
    id: element
    objectName: "element"
    property int alignment: Qt.AlignHCenter
    Layout.alignment: alignment
    property bool fillWidth: true
    property bool fillHeight: false
    property string topMargin: "0"
    property string rightMargin: "0"
    property string bottomMargin: "0"
    property string leftMargin: "0"
    Layout.fillWidth: fillWidth
    Layout.fillHeight: fillHeight
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin
// <property>

// **closing_key**
} // Element id: element
"""


class Element(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__class_name = 'Element'
        self.__id = 'element'
        self.__qml = qml_code

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):

            if line.strip().startswith('id:'):
                qml_lines.append(f'id: {object_id}')

            elif line.strip().startswith('objectName:'):
                qml_lines.append(f'objectName: "{object_id}"')

            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

    @property
    def class_name(self) -> str:
        """..."""
        return self.__class_name

    @class_name.setter
    def class_name(self, class_name: str) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().startswith(f'{self.__class_name} {{'):
                qml_lines.append(f'{class_name} {{')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__class_name = class_name
