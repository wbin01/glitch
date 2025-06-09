#/usr/bin/env python3
from .element import Element


class Label(Element):
    """..."""
    def __init__(
            self, text: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text

        self.class_name = 'Label'

        self.qml = self.qml.replace(
            '\n// <property>',
            f'\n    text: "{self.__text}"'
            '\n// <property>')
