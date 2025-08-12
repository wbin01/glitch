#!/usr/bin/env python3


qml_code = """
Item {
    id: ui  // ID
    objectName: "ui"  // Object name
    property string className: "UI"  // Class name
    property string baseClass: "UI"  // Base class
    property string styleClass: "UI"  // Style class
    property string baseStyle: "UI"  // Base style

    // Element header

    height: 30
    width: 100

    property int alignment: Qt.AlignHCenter
    Layout.alignment: alignment

    property bool fillWidth: true
    property bool fillHeight: false
    Layout.fillWidth: fillWidth
    Layout.fillHeight: fillHeight
    
    Layout.preferredWidth: width
    Layout.preferredHeight: height

    // Layout header

    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin

    // Frame header

    // Property
}
"""


class UI(object):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        self.__qml = qml_code
        self.__obj = None
        self.__name = 'UI'
        self.__style_class = 'UI'
        self.__base_style_class = 'UI'
        self.class_id('UI')

    @property
    def style_class(self) -> str:
        """..."""
        return self.__style_class

    @style_class.setter
    def style_class(self, style_class: str) -> None:
        # TODO: obj
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// Style class'):
                qml_lines.append(
                    f'    property string styleClass: "{style_class}"  '
                    '// Style class')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__style_class = style_class

    @property
    def _id(self) -> str:
        """Element identifier."""
        return self.__id

    @_id.setter
    def _id(self, id_: int) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// ID'):
                qml_lines.append(f'    id: {id_}  // ID')
            elif line.strip().endswith('// Object name'):
                qml_lines.append(f'    objectName: "{id_}"  // Object name')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__id = id_

    @property
    def _name(self) -> str:
        """Element type name."""
        return self.__name

    @_name.setter
    def _name(self, name: str) -> None:
        qml_lines = []
        for line in self.__qml.split('\n'):
            if line.strip().endswith('// Class name'):
                qml_lines.append(
                    f'    property string className: "{name}"  // Class name')
            else:
                qml_lines.append(line)

        self.__qml = '\n'.join(qml_lines)
        self.__name = name

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

    def class_id(self, class_id: str) -> None:
        """..."""
        # Only __init__
        self._qml = self._qml.replace(
            f'property string baseStyle: "{self.__base_style_class}"',
            f'property string baseStyle: "{class_id}"')
        self.__base_style_class = self._name

        self._id = '_' + str(id(self))
        self._name = class_id

    def __str__(self) -> str:
        return "<class 'UI'>"
