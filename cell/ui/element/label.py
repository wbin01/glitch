#!/usr/bin/env python3
from ..base import Element


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
        self._qml = (
            '\nLabel {'
            '\n    id: label  // <id>'
            '\n    objectName: "label"  // <objectName>'
            '\n    property string qmlType: "Label"  // <className>'
            '\n    property string baseClass: "Element"  // <baseClass>'
            f'\n    text: "{self.__text}"'
            '\n    color: "#fff"'
            '\n    property int topMargin: 0'
            '\n    property int rightMargin: 0'
            '\n    property int bottomMargin: 0'
            '\n    property int leftMargin: 0'
            '\n    Layout.topMargin: topMargin'
            '\n    Layout.rightMargin: rightMargin'
            '\n    Layout.bottomMargin: bottomMargin'
            '\n    Layout.leftMargin: leftMargin'
            '\n}  // <suffix_id>\n')

        # self.id = '_' + str(id(self))
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
