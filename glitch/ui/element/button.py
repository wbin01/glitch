#!/usr/bin/env python3
from ..base import Element, IconMixin
from ...core.signal import Signal
from ...enum.event import Event


header = """
Button {
    id: button  // ID
    objectName: "button"  // Object name
    property string className: "Button"  // Class name
    property string baseClass: "Element"  // Base class
    property string styleClass: "Button"  // Style class
    property string baseStyle: "Button"  // Base style
"""

properties = """
    text: "<text>"
    checkable: false
    checked: false
"""


class Button(IconMixin, Element):
    """Button Element."""
    def __init__(
            self, text: str = '', icon: str = None, icon_size: int = 16,
            *args, **kwargs) -> None:
        """
        :param text: Button text string.
        :param icon: Icon name or path string.
        """
        super().__init__(icon=icon, icon_size=icon_size, *args, **kwargs)
        self.__callbacks = {}

        # Args
        self.__text = text
        self.__checkable = False
        self.__checked = False

        # Signals
        self.mouse_press_signal = Signal()
        self.mouse_hover_signal = Signal()
        self.application_frame_signal.connect(self.__application_frame_signal)

        # QML
        self._qml = header + self._qml.split('// Element header')[1].replace(
            '\n    // Property', properties.replace('<text>', self.__text))
        self.class_id('Button')
        self.style_class = 'Button'

    @property
    def checkable(self) -> bool:
        """..."""
        return self.__checkable

    @checkable.setter
    def checkable(self, checkable: bool) -> None:
        if self._obj:
            self._obj.setProperty('checkable', checkable)
        else:
            last_checkable = 'true' if self.__checkable else 'false'
            checkable_str = 'true' if checkable else 'false'
            self._qml = self._qml.replace(
                f'checkable: {last_checkable}', f'checkable: {checkable_str}')
        self.__checkable = checkable

    @property
    def checked(self) -> bool:
        """..."""
        return self.__checked

    @checked.setter
    def checked(self, checked: bool) -> None:
        if self._obj:
            self._obj.setProperty('checked', checked)
        else:
            __checked_str = 'true' if self.__checked else 'false'
            checked_str = 'true' if checked else 'false'
            self._qml = self._qml.replace(
                f'checked: {__checked_str}', f'checked: {checked_str}')

        self.__checked = checked

    @property
    def text(self) -> str:
        """Button text string."""
        return self.__text

    @text.setter
    def text(self, text: str) -> None:
        if self._obj:
            self._obj.setProperty('text', text)
        else:
            self._qml = self._qml.replace(
                f'text: "{self.__text}"', f'text: "{text}"')
        self.__text = text

    def callbacks(self) -> dict:
        """The functions used in the `connect` method.

        The `connect` method organizes the received functions into a 
        dictionary organized by the type of event they are associated with.
        """
        return self.__callbacks

    def is_mouse_hover(self) -> bool:
        """If the mouse is hovering over this button.

        Returns `True` if the mouse is hovering, otherwise it returns `False`.
        """
        if self._obj:
            return self._obj.property('hovered')
        return False

    def __application_frame_signal(self) -> None:
        if not self._obj:
            return

        self._obj.clicked.connect(
            lambda: self.mouse_press_signal.emit())
        self._obj.hoveredChanged.connect(
            lambda: self.mouse_hover_signal.emit())

    def __str__(self) -> str:
        return "<class 'Button'>"
