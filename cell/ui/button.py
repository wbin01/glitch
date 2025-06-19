#/usr/bin/env python3
import pathlib

from .element import Element


class Button(Element):
    """..."""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__path = pathlib.Path(__file__).parent.parent

        # Args
        self.__text = text
        self.__icon = self.__path/'static'/'icons'/f'{icon}.svg'

        # Set
        self.qml = (
            '\nButton {'
            '\n    id: button  // <id>'
            '\n    objectName: "button"  // <objectName>'
            '\n    property string qmlType: "Button"  // <className>'
            f'\n    text: "{self.__text}"'
            f'\n    iconSource: "{self.__icon}"'
            '\n}  // <suffix_id>\n')

        self.object_id = '_' + str(id(self))
        self.class_name = 'Button'
        self.text = self.__text
        self.icon = icon

        self.callables = {}

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

    @property
    def icon(self) -> str:
        """..."""
        return self.__icon

    @icon.setter
    def icon(self, name: str) -> None:
        icon = self.__path/'static'/'icons'/f'{name}.svg'
        self.qml = self.qml.replace(
            f'\n    iconSource: "{self.__icon}"',
            f'\n    iconSource: "{icon}"')
        self.__icon = icon

    def connect(self, func: callable) -> None:
        self.callables['clicked'] = func
