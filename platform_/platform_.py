#!/usr/bin/env python3
import os

from .icons import Icons
from .os_desk import OSDesk
from .style import Style
from ..tools import color_converter, DesktopFile


class Platform(object):
    """..."""
    def __init__(self):
        self.__os_desk = OSDesk()
        self.__icons = Icons(self.__os_desk.desktop_environment)
        self.__style = Style()

        # Properties
        self.__accent_color = None
        self.__dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self.style['[MainFrame]']['background_color']))
        self.__icon_theme = None

        self.__de = None
        self.__os = None
        self.__display_server = None

        # Set
        self.__kwinrc = None
        self.__breezerc = None
        self.__kde_globals = None

    @property
    def global_menu(self) -> bool:
        """..."""
        if not self.__kwinrc:
            self.__set__kwinrc()

        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            return True if self.__kwinrc[group][key] == 'true' else False

        return False

    @property
    def accent_color(self) -> str:
        """..."""
        if not self.__accent_color:
            self.__accent_color = self.__style.accent_color()
        return self.__accent_color

    @accent_color.setter
    def accent_color(self, accent_color: str) -> None:
        self.__accent_color = accent_color

    @property
    def de(self) -> str:
        """..."""
        if not self.__de:
            self.__de = self.__os_desk.desktop_environment

        return self.__de

    @de.setter
    def de(self, desktop_environment: str | None) -> None:
        self.__de = desktop_environment

    @property
    def display_server(self) -> str:
        if not self.__display_server:
            self.__display_server = self.__os_desk.display_server

        return self.__display_server

    @display_server.setter
    def display_server(self, display_server: str | None) -> None:
        self.__display_server = display_server

    @property
    def icon_theme(self) -> str | None:
        """..."""
        if not self.__icon_theme:
            self.__icon_theme = self.__icons.icon_theme()
        
        return self.__icon_theme

    @icon_theme.setter
    def icon_theme(self, icon_theme: str | None) -> None:
        """..."""
        self.__icon_theme = icon_theme

    @property
    def os(self) -> str:
        """..."""
        if not self.__os:
            self.__os = self.__os_desk.operational_system

        return self.__os

    @os.setter
    def os(self, operational_system: str | None) -> None:
        self.__os = operational_system

    @property
    def style(self) -> dict:
        """..."""
        if not self.__style:
            self.__style = Style()

        return self.__style.style

    @style.setter
    def style(self, style: dict | None) -> None:
        self.__style = style

    def icon_source(self, source: str | None, dark: bool = None) -> str:
        return self.__icons.icon_source(source, dark=dark)

    def icon_theme_variant(
            self, icon_theme: str = None, dark: bool = None) -> str:
        """..."""
        if not icon_theme: icon_theme = self.icon_theme
        if dark is None:
            dark = False if self.__dark else True

        return self.__icons.icon_theme_variant(icon_theme, dark)

    def __set__kwinrc(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'kwinrc')
        self.__kwinrc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})

    def __set__breezerc(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'breezerc')
        self.__breezerc = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})
    
    def __set__kde_globals(self) -> dict:
        filerc = os.path.join(os.environ['HOME'], '.config', 'kdeglobals')
        self.__kde_globals = (
            DesktopFile(url=filerc).content if os.path.isfile(filerc) else {})
