#!/usr/bin/env python3
from .icons import Icons
from .os_desk import OSDesk
from .style import Style


class Platform(object):
    """..."""
    def __init__(self):
        self.__os_desk = OSDesk()
        self.__icons = Icons(self.__os_desk.desktop_environment)
        self.__style = Style()

        self.__icon_theme = None

    @property
    def de(self) -> str:
        """..."""
        return self.__os_desk.operational_system

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
    def os(self) -> str:
        """..."""
        return self.__os_desk.desktop_environment

    @property
    def style(self) -> dict:
        """..."""
        return self.__style.style()
