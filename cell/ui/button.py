#/usr/bin/env python3
from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text
        self.__icon = icon
        self.qml = (
            '\n'
            '\nButton {'
            f'\n    id: {self.object_id}'
            f'\n    objectName: "{self.object_id}"'
            f'\n    text: "{self.__text}"'
            f'\n    iconSource: "{self.__icon}"'
            '\n// **closing_key**'
            f'\n}} // Button id: {self.object_id}')
