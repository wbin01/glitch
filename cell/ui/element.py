#/usr/bin/env python3


qml_code = """
Item {
    id: element  // <id>
    objectName: "element"  // <objectName>
    property string qmlType: "Item"  // <className>
    property int alignment: Qt.AlignHCenter
    Layout.alignment: alignment
    property bool fillWidth: true
    property bool fillHeight: false
    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0
    Layout.fillWidth: fillWidth
    Layout.fillHeight: fillHeight
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin
} // <suffix_id>
"""


class Element(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__qml = qml_code
        self.object_id = '_' + str(id(self))
        self.class_name = 'Element'

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// <id>'):
                qml_lines.append(f'    id: {object_id}  // <id>')

            elif line.strip().endswith('// <objectName>'):
                qml_lines.append(
                    f'    objectName: "{object_id}"  // <objectName>')

            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines).replace('<suffix_id>', object_id)
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
            if line.strip().endswith('// <className>'):
                qml_lines.append(
                    f'    property string qmlType: "{class_name}"  '
                    '// <className>')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__class_name = class_name
