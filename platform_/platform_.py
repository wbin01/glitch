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

        self.__light_suffixes = ['-light', '-Light', ' light', ' Light']
        self.__dark_suffixes = ['-dark', '-Dark', ' dark', ' Dark']
        self.__icon_theme_paths = [
            '/usr/share/icons/', '/home/user/.local/share/icons/',
            '/home/user/.icons/']
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

    def _variant_icon_theme(
            self, theme: str, frame_is_dark: bool) -> str:
        """Dark or light variant icon theme"""
        icon_theme = ''
        for path in self.__icon_theme_paths:
            for suffix in self.__dark_suffixes:
                
                if frame_is_dark and 'dark' not in theme.lower():
                    if 'light' in theme.lower():
                        
                        for x in self.__light_suffixes:
                            theme = theme.replace(x, '')

                    if Path(path + theme + suffix).exists():
                        icon_theme = theme + suffix

                elif not frame_is_dark and 'dark' in theme.lower():
                    temp = theme.replace(suffix, '')
                    if Path(path + temp).exists() and 'dark' not in temp.lower():
                        icon_theme = temp

        return icon_theme
