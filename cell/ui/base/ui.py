#!/usr/bin/env python3


qml_code = """
Item {
    id: ui  // <id>
    objectName: "ui"  // <objectName>
    property string qmlType: "UI"  // <className>
    property string baseClass: "UI"  // <baseClass>

    property int alignment: Qt.AlignHCenter
    Layout.alignment: alignment

    property bool fillWidth: true
    property bool fillHeight: false
    Layout.fillWidth: fillWidth
    Layout.fillHeight: fillHeight

    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin

    // <property>
}
"""


class UI(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.__qml = qml_code
        self.__id = '_' + str(id(self))
        self.__element_type = 'UI'
        self.__obj = None

        self.id = self.__id
        self._element_type = self.__element_type

    @property
    def id(self) -> str:
        """Element identifier."""
        return self.__id

    @id.setter
    def id(self, id_: int) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// <id>'):
                qml_lines.append(f'    id: {id_}  // <id>')
            elif line.strip().endswith('// <objectName>'):
                qml_lines.append(
                    f'    objectName: "{id_}"  // <objectName>')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)  # .replace('<suffix_id>', id_)
        self.__id = id_

    @property
    def _element_type(self) -> str:
        """Element type name."""
        return self.__element_type

    @_element_type.setter
    def _element_type(self, element_type: str) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// <className>'):
                qml_lines.append(
                    f'    property string qmlType: "{element_type}"  '
                    '// <className>')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__element_type = element_type

    @property
    def _obj(self) -> str:
        """Qt Object.

        Internal object manipulated by the wrapper class.
        """
        return self.__obj

    @_obj.setter
    def _obj(self, obj: str) -> None:
        self.__obj = obj

    @property
    def _qml(self) -> str:
        """Qml code.

        Internal Qml handled by the wrapper class.
        """
        return self.__qml

    @_qml.setter
    def _qml(self, qml: str) -> None:
        self.__qml = qml

    def __str__(self) -> str:
        return "<class 'UI'>"
