#/usr/bin/env python3
import pathlib

from .element import Element
from ..enum.event import Event


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
            '\n    property int topMargin: 0'
            '\n    property int rightMargin: 0'
            '\n    property int bottomMargin: 0'
            '\n    property int leftMargin: 0'
            '\n    Layout.topMargin: topMargin'
            '\n    Layout.rightMargin: rightMargin'
            '\n    Layout.bottomMargin: bottomMargin'
            '\n    Layout.leftMargin: leftMargin'
            '\n}  // <suffix_id>\n')

        self.object_id = '_' + str(id(self))
        self._element_name = 'Button'
        self.text = self.__text
        self.icon = icon

        self.callbacks = {}

    @property
    def icon(self) -> str:
        """..."""
        if self._obj:
            return self.__icon
        return self.__icon

    @icon.setter
    def icon(self, name: str) -> None:
        if self._obj:
            self._obj.setProperty('icon', name)
            return
        
        icon = self.__path/'static'/'icons'/f'{name}.svg'
        self.qml = self.qml.replace(
            f'\n    iconSource: "{self.__icon}"',
            f'\n    iconSource: "{icon}"')
        self.__icon = icon

    @property
    def text(self) -> str:
        """..."""
        if self._obj:
            return self._obj.property('text')
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        if self._obj:
            self._obj.setProperty('text', text)
            return
        
        self.qml = self.qml.replace(
            f'\n    text: "{self.__text}"',
            f'\n    text: "{text}"')
        self.__text = text

    def connect(
            self, method: callable, event: Event = Event.MOUSE_PRESS) -> None:
        """..."""
        if self._obj:
            if event == Event.MOUSE_PRESS:
                self._obj.clicked.connect(method)
            elif event == Event.MOUSE_HOVER:
                self._obj.hoveredChanged.connect(method)
            return

        self.callbacks[event] = method

    def hover(self) -> bool:
        if self._obj:
            return self._obj.property('hovered')

        return False
