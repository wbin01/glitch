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
        self.__control_buttons_order = None
        self.__dark_variant = None
        self.__de = None
        self.__display_server = None
        self.__global_menu = None
        self.__icon_theme = None
        self.__os = None

        # Set
        self.__breezerc = None
        self.__kde_globals = None
        self.__kwinrc = None

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
    def control_buttons_order(self) -> tuple:
        """XAI M -> (2, 1, 0), (3,)

        Close     Max       Min       Icon      Above all
        X = 2     A = 1     I = 0     M = 3     F = 4

        (2, 1, 0), (3,) -> [Close Max Min ............. Icon]
        """
        if self.__control_buttons_order:
            return self.__control_buttons_order

        if self.de != 'plasma':
            self.__control_buttons_order = ('close', 'max', 'min'), ('icon',)
            return self.__control_buttons_order  # (2, 1, 0), (3,)

        if not self.__kwinrc:
            self.__set__kwinrc()

        left_buttons = 'M'  # M = icon, F = above all
        right_buttons = 'IAX'  # X = close, A = max, I = min

        kdecoration = '[org.kde.kdecoration2]'
        buttons_on_left, buttons_on_right = 'ButtonsOnLeft', 'ButtonsOnRight'
        if kdecoration in self.__kwinrc:
            if buttons_on_left in self.__kwinrc[kdecoration]:
                left_buttons = self.__kwinrc[kdecoration][buttons_on_left]

            if buttons_on_right in self.__kwinrc[kdecoration]:
                right_buttons = self.__kwinrc[kdecoration][buttons_on_right]

        # d = {'X': 2, 'A': 1, 'I': 0, 'M': 3}
        d = {'X': 'close', 'A': 'max', 'I': 'min', 'M': 'icon'}
        self.__control_buttons_order = tuple(
            d[x] for x in left_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M'), tuple(
            d[x] for x in right_buttons
            if x == 'X' or x == 'A' or x == 'I' or x == 'M')

        return self.__control_buttons_order

    @property
    def dark_variant(self) -> bool:
        """..."""
        if self.__dark_variant is not None:
            return self.__dark_variant

        self.__dark_variant = color_converter.is_dark(
            color_converter.hex_to_rgba(
                self.style['[MainFrame]']['background_color']))

        return self.__dark_variant

    @dark_variant.setter
    def dark_variant(self, dark_variant: bool) -> None:
        self.__dark_variant = dark_variant

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
    def global_menu(self) -> bool:
        """..."""
        if self.__global_menu is not None:
            return self.__global_menu

        if not self.__kwinrc:
            self.__set__kwinrc()

        self.__global_menu = False
        group, key = '[Windows]', 'BorderlessMaximizedWindows'
        if group in self.__kwinrc and key in self.__kwinrc[group]:
            if self.__kwinrc[group][key] == 'true': self.__global_menu = True

        return self.__global_menu

    @global_menu.setter
    def global_menu(self, global_menu: bool) -> None:
        self.__global_menu = global_menu

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
            dark = False if self.__dark_variant else True

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
