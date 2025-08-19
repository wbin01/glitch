#!/usr/bin/env python3
import pathlib

from xdg import IconTheme

from ..base import Element
from ...core.application_style import style_value
from ...enum.event import Event
from ...platform_ import OSDesk, Icons
from ...tools import color_converter


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
    iconSource: <icon>
    checkable: false
    checked: false
"""


class Button(Element):
    """Button Element."""
    def __init__(
            self, text: str = '', icon: str = None, icon_size: int = 16,
            *args, **kwargs) -> None:
        """
        :param text: Button text string.
        :param icon: Icon name or path string.
        """
        super().__init__(*args, **kwargs)
        self.__callbacks = {}
        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon_path = self.__path / 'static' / 'icons' / 'linux'
        self.__platform_icons = Icons(OSDesk().desktop_environment)
        self.__icon_theme = 'hicolor'
        self.application_frame_signal.connect(self.__update_icon)

        # Args
        self.__text = text
        self.__icon_size = icon_size
        self.__icon = self.__get_icon_path(icon)
        self.__checkable = False
        self.__checked = False

        # QML
        self._qml = header + self._qml.split(
            '// Element header')[1].replace('\n    // Property',
            properties.replace(
                '<text>', self.__text).replace('<icon>', self.__icon))
        self.class_id('Button')
        self.style_class = 'Button'

        # Properties
        self.icon = icon

    def __update_icon(self) -> None:
        # Fix: Plasma updates icons without registering
        if hasattr(self._application_frame, '_platform'):
            self.__icon_theme = self._application_frame._platform.icon_theme

            if 'breeze' not in self.__icon_theme:
                return
            
            header = '[' + self._application_frame._name + ']'
            is_dark = color_converter.is_dark(color_converter.hex_to_rgba(
                self._application_frame.style[header]['background_color']))

            self.__icon_theme = 'breeze-dark' if is_dark else 'breeze'
            if self.__icon_theme == 'breeze-dark':
                self._application_frame._platform.icon_theme = 'breeze-dark'

                icon = self.__icon.strip('"')
                icon_path = IconTheme.getIconPath(
                    iconname=pathlib.Path(icon).stem,
                    size=self.__icon_size,
                    theme=self.__icon_theme,
                    extensions=['png', 'svg', 'xpm'])
                self.icon = icon_path if icon_path else icon

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
    def icon(self) -> str:
        """Icon name or path string."""
        return self.__icon

    @icon.setter
    def icon(self, icon: str) -> None:

        icon = self.__get_icon_path(icon)

        if self._obj:
            self._obj.setProperty('iconSource', icon.strip('"'))
        else:
            self._qml = self._qml.replace(
                f'iconSource: {self.__icon}', f'iconSource: {icon}')
        self.__icon = icon

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

        self.__callbacks[event] = method

    def is_mouse_hover(self) -> bool:
        """If the mouse is hovering over this button.

        Returns `True` if the mouse is hovering, otherwise it returns `False`.
        """
        if self._obj:
            return self._obj.property('hovered')
        return False

    def __get_icon_path(self, icon_name: str | None) -> str | None:
        if not icon_name:
            return '""'

        elif '/' in icon_name:
            if not pathlib.Path(icon_name).exists():
                return '""'
            return f'"{icon_name}"'

        else:
            icon_path = IconTheme.getIconPath(
                iconname=icon_name,
                size=self.__icon_size,
                # theme=self.__platform_icons.icon_theme(),
                theme=self.__icon_theme,
                extensions=['png', 'svg', 'xpm'])

            if icon_path:
                return f'"{icon_path}"'

            icon = icon_name + '.svg'
            path = self.__icon_path / icon
            return f'"{path}"' if path.exists() else '""'
                # impl callback
        """
        IconTheme.getIconPath(
            iconname=self.__icon_name,
            size=22,
            theme='breeze-dark',
            extensions=['png', 'svg', 'xpm']

        from PySide6.QtGui import QIcon
        icon = QIcon.fromTheme("document-save")
        
        ----
        Self linux impl
        
        ICON PATH
            User:
                Gtk
                /home/user/.icons/icon-theme/22x22/actions/icon-name.svg
                Qt
                /home/user/.icons/icon-theme/actions/22/icon-name.svg
            
            Gtk
            /usr/share/icons/icon-theme/22x22/actions/icon-name.svg
            Qt
            /usr/share/icons/icon-theme/actions/22/icon-name.svg
            
            Default sys
            /usr/share/icons/hicolor/22x22/actions/icon-name.png
            Default lib
            self.__icon_path / document-save.svg

        ROADMAP
            loop paths:
                check for: Gtk Qt icon-name icon-theme.png .svg
            else:
                or: Default sys
                or: Default lib
                or: callback-icon-path
        """

    def __str__(self) -> str:
        return "<class 'Button'>"
