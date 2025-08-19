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

    def de(self) -> str:
        """..."""
        return self.__os_desk.operational_system

    def icon_theme(self) -> str | None:
        """..."""
        return self.__icons.icon_theme()

    def os(self) -> str:
        """..."""
        return self.__os_desk.desktop_environment

    def style(self) -> dict:
        """..."""
        return self.__style.style()
