#/usr/bin/env python3
from .element import Element


class Label(Element):
    """..."""
    def __init__(
            self, text: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        # Args
        self.__text = text

        # Set
        self.qml = (
            '\nLabel {'
            '\n    id: label  // <id>'
            '\n    objectName: "label"  // <objectName>'
            '\n    property string qmlType: "Label"  // <className>'
            f'\n    text: "{self.__text}"'
            '\n    color: "#fff"'
            '\n}  // <suffix_id>\n')

        self.object_id = '_' + str(id(self))
        self.class_name = 'Label'
        self.text = self.__text

    @property
    def text(self) -> str:
        """..."""
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        self.qml = self.qml.replace(
            f'\n    text: "{self.__text}"',
            f'\n    text: "{text}"')
        self.__text = text
