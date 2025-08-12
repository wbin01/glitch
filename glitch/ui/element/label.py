#!/usr/bin/env python3
from ..base import Element
from ...enum import Size


header = """
Label {
    id: label  // ID
    objectName: "label"  // Object name
    property string className: "Label"  // Class name
    property string baseClass: "Element"  // Base class
    property string styleClass: "Label"  // Style class
    property string baseStyle: "Label"  // Base style
"""

properties = """
    text: "<text>"
    color: "#fff"

    // Layout.fillWidth: true
    // Layout.preferredHeight: 80
    // horizontalAlignment: Text.AlignHCenter
    // verticalAlignment: Text.AlignVCenter
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

        # QML
        self._qml = header + self._qml.split(
            '// Element header')[1].replace('\n    // Property',
                properties.replace('<text>', self.__text))
        self.class_id('Label')
        self.style_class = 'Label'

        # Properties
        self.text = self.__text
        self.size = None, 20

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
