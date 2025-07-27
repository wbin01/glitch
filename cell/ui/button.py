#/usr/bin/env python3
import pathlib

from .element import Element
from ..enum.event import Event


class Button(Element):
    """Button Element"""
    def __init__(
            self, text: str = '', icon: str = '', *args, **kwargs) -> None:
        """
        :param text: Button text string.
        :param icon: Icon name or path string.
        """
        super().__init__(*args, **kwargs)
        self.__path = pathlib.Path(__file__).parent.parent

        # Args
        self.__text = text
        self.__icon = self.__path/'static'/'icons'/f'{icon}.svg'

        # Set
        self._qml = (
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

        self.id = '_' + str(id(self))
        self._element_name = 'Button'
        self.text = self.__text
        self.icon = icon

        self.callbacks = {}

    @property
    def icon(self) -> str:
        """Icon name or path string."""
        if self._obj:
            return self.__icon
        return self.__icon

    @icon.setter
    def icon(self, name: str) -> None:
        if self._obj:
            self._obj.setProperty('icon', name)
            return
        
        icon = self.__path/'static'/'icons'/f'{name}.svg'
        self._qml = self._qml.replace(
            f'\n    iconSource: "{self.__icon}"',
            f'\n    iconSource: "{icon}"')
        self.__icon = icon

    @property
    def text(self) -> str:
        """Button text string."""
        if self._obj:
            return self._obj.property('text')
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        if self._obj:
            self._obj.setProperty('text', text)
            return
        
        self._qml = self._qml.replace(
            f'\n    text: "{self.__text}"',
            f'\n    text: "{text}"')
        self.__text = text

    def connect(
            self, method: callable, event: Event = Event.MOUSE_PRESS) -> None:
        """Connect the button to a method.

        Pass a method to be executed when interacting with the button.
        Alternatively, use an event like `Event.MOUSE_HOVER` or 
        `Event.MOUSE_WHEEL` to configure when the button will use the method.

        :param method: method to be executed when interacting with the button.
        :param event: Enum like `Event.MOUSE_HOVER` or `Event.MOUSE_WHEEL`
        """
        if self._obj:
            if event == Event.MOUSE_PRESS:
                self._obj.clicked.connect(method)
            elif event == Event.MOUSE_HOVER:
                self._obj.hoveredChanged.connect(method)
            return

        self.callbacks[event] = method

    def is_mouse_hover(self) -> bool:
        """If the mouse is hovering over this button.

        Returns `True` if the mouse is hovering, otherwise it returns `False`.
        """
        if self._obj:
            return self._obj.property('hovered')

        return False
