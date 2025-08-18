#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from ..tools import DesktopFile


class Icons(object):
    """Information about operating system icons."""
    def __init__(self, desktop_environment: str) -> None:
        """
        :param desktop_environment: DE name, like 'plasma' or 'mate'.
        """
        self.__desktop_environment = desktop_environment
        self.__plasma_icon_theme = None
        self.__gtk_icon_theme = None

    def icon_theme(self) -> str | None:
        """Icon theme name.

        Retrieve the name of the system icon theme.
        """
        if self.__desktop_environment == 'plasma':

            if self.__plasma_icon_theme:
                return self.__plasma_icon_theme

            kdeglobals = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
            if kdeglobals.exists():
                ini = DesktopFile(kdeglobals)

                if not '[Icons]' in ini.content:
                    self.__plasma_icon_theme = 'breeze'
                    return self.__plasma_icon_theme

                if not 'Theme' in ini.content['[Icons]']:
                    self.__plasma_icon_theme = 'breeze'
                    return self.__plasma_icon_theme
                
                self.__plasma_icon_theme = ini.content['[Icons]']['Theme']
                return self.__plasma_icon_theme

        if self.__desktop_environment == 'mate':
            if self.__gtk_icon_theme:
                return self.__gtk_icon_theme

                gtk_icons = subprocess.getoutput(
                    'dconf read /org/mate/desktop/interface/icon-theme').strip(
                    "'")
                self.__gtk_icon_theme = gtk_icons if gtk_icons else None
                return self.__gtk_icon_theme

        if self.__desktop_environment == 'gnome':
            if self.__gtk_icon_theme:
                return self.__gtk_icon_theme

            gtk_icons = subprocess.getoutput(
                'gsettings get org.gnome.desktop.interface icon-theme').strip(
                "'")
            self.__gtk_icon_theme = gtk_icons if gtk_icons else None
            return self.__gtk_icon_theme

    def __str__(self) -> str:
        return "<class 'Icons'>"


if __name__ == '__main__':
    icons = PlatformIcons('plasma')
    print(icons.icon_theme())
