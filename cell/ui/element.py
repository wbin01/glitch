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
        self.__id = '_' + str(id(self))
        self.__element_type = 'Element'
        self.__obj = None

        self.object_id = self.__id
        self._element_type = self.__element_type

    @property
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        A tuple with the 4 margin values. The values are in clockwise
        order: top, right, bottom and left respectively.

        Get:
            (5, 10, 5, 10)

        Set:
            It is not mandatory to pass all the values, the last value will be 
            used to fill in the missing ones:

            `margins = 5` is equivalent to `margins = 5, 5, 5, 5`
            `margins = 5, 10` is equivalent to `margins = 5, 10, 10, 10`

            Use `None` for a value to be automatic. `None` indicates that the 
            value is the same as before. Example:

                # Change only the vertical margins (top and bottom)
                `margins = 10, None, 10, None`
        """
        margins = {
            'topMargin': 0, 'rightMargin': 0,
            'bottomMargin': 0, 'leftMargin': 0}

        for line in self.__qml.split('\n'):
            for margin in margins:
                if 'property int ' + margin in line:
                    margins[margin] = int(line.split(':')[-1].strip())
        
        return (
            margins['topMargin'], margins['rightMargin'],
            margins['bottomMargin'], margins['leftMargin'])

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            if not margins.isdigit():
                return
            margins = int(magins)

        prev_margins = self.margins

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = prev_margins[0] if top is None else top
        right = prev_margins[1] if right is None else right
        bottom = prev_margins[2] if bottom is None else bottom
        left = prev_margins[3] if left is None else left

        qml = []
        for line in self.__qml.split('\n'):
            if 'property int topMargin:' in line:
                qml.append(f'property int topMargin: {top}')
            elif 'property int rightMargin:' in line:
                qml.append(f'property int rightMargin: {right}')
            elif 'property int bottomMargin:' in line:
                qml.append(f'property int bottomMargin: {bottom}')
            elif 'property int leftMargin:' in line:
                qml.append(f'property int leftMargin: {left}')
            else:
                qml.append(line)
        self.__qml = '\n'.join(qml)

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
    def _element_type(self) -> str:
        """..."""
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
        """..."""
        return self.__obj

    @_obj.setter
    def _obj(self, obj: str) -> None:
        self.__obj = obj
