#!/usr/bin/env python3
from ..base import Element


qml = """
Label {
    id: label  // <id>
    objectName: "label"  // <objectName>
    property string qmlType: "Label"  // <className>
    property string baseClass: "Element"  // <baseClass>
    text: "<text>"
    color: "#fff"
    property int topMargin: 0
    property int rightMargin: 0
    property int bottomMargin: 0
    property int leftMargin: 0
    Layout.topMargin: topMargin
    Layout.rightMargin: rightMargin
    Layout.bottomMargin: bottomMargin
    Layout.leftMargin: leftMargin
}
"""


class Label(Element):
    """Label Element"""
    def __init__(
            self, text: str = '', *args, **kwargs) -> None:
        """
        :param text: Label text string.
        """
        super().__init__(*args, **kwargs)
        # Args
        self.__text = text

        # Set
        self._qml = qml.replace('<text>', self.__text)
        self.id = f'_{id(self)}'
        self._element_type = 'Label'
        self.text = self.__text

    @property
    def text(self) -> str:
        """Label text string."""
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        if self._obj:
            self._obj.setProperty('text', text)
        else:
            self._qml = self._qml.replace(
                f'\n    text: "{self.__text}"',
                f'\n    text: "{text}"')
        
        self.__text = text

    def __str__(self) -> str:
        return "<class 'Label'>"
