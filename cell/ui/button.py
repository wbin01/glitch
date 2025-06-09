#/usr/bin/env python3
import pathlib

from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = text

        path = pathlib.Path(__file__).parent.parent
        self.__icon = path/'static'/'icons'/f'{icon}.svg'

        self.class_name = 'Button'

        self.qml = self.qml.replace(
            '\n// <property>',
            f'\n    text: "{self.__text}"'
            f'\n    iconSource: "{self.__icon}"'
            '\n// <property>')
