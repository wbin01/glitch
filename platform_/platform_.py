#!/usr/bin/env python3
from pathlib import Path

from .icons import Icons
from .os_desk import OSDesk
from .style import Style
from ..tools import color_converter


class Platform(object):
    """..."""
    def __init__(self):
        self.__os_desk = OSDesk()
        self.__icons = Icons(self.__os_desk.desktop_environment)
        self.__style = Style()
        self.__accent_color = None

        self.__dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self._style['[AppFrame]']['background_color']))
        self.__icon_theme = None

    @property
    def _accent_color(self) -> str:
        """..."""
        if not self.__accent_color:
            self.__accent_color = self.__style.accent_color()
        return self.__accent_color

    @property
    def _de(self) -> str:
        """..."""
        return self.__os_desk.desktop_environment
    @property
    def _display_server(self) -> str:
        return self.__os_desk.display_server

    @property
    def icon_theme(self) -> str | None:
        """..."""
        if not self.__icon_theme:
            self.__icon_theme = self.__icons.icon_theme()
        return self.__icon_theme

    @icon_theme.setter
    def icon_theme(self, icon_theme: str) -> None:
        """..."""
        self.__icon_theme = icon_theme

    @property
    def _os(self) -> str:
        """..."""
        return self.__os_desk.operational_system

    @property
    def _style(self) -> dict:
        """..."""
        return self.__style.style()

    def icon_source(self, source: str | None) -> str:
        return self.__icons.icon_source(source)

    def icon_theme_variant(
            self, icon_theme: str = None, dark: bool = None) -> str:
        """..."""
        if not icon_theme: icon_theme = self.icon_theme
        if dark is None:
            dark = False if self.__dark else True

        return self.__icons.icon_theme_variant(icon_theme, dark)
