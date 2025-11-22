#!/usr/bin/env python3
import os
import sys
from pathlib import Path

from xdg import IconTheme

from ..tools import DesktopFile


class Icons(object):
    """Information about operating system icons."""
    def __init__(self, desktop_environment: str) -> None:
        """
        :param desktop_environment: DE name, like 'plasma' or 'mate'.
        """
        self.__desktop_environment = desktop_environment
        self.__icon_theme = None

        self.__path = Path(__file__).parent.parent
        self.__icon_path = self.__path / 'static' / 'icons' / 'linux'
        self.__icon_empty = self.__icon_path / 'empty.svg'

        self.__light_suffixes = ['-light', '-Light', ' light', ' Light']
        self.__dark_suffixes = ['-dark', '-Dark', ' dark', ' Dark']
        self.__icon_theme_paths = [
            '/usr/share/icons/', '/home/user/.local/share/icons/',
            '/home/user/.icons/']

    def clear_cache(self) -> None:
        """Clear properties cache"""
        self.__icon_theme = None

    def icon_theme(self) -> str | None:
        """Icon theme name.

        Retrieve the name of the system icon theme.
        """
        if self.__desktop_environment == 'plasma':

            if self.__icon_theme:
                return self.__icon_theme

            kdeglobals = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
            if kdeglobals.exists():
                ini = DesktopFile(kdeglobals)

                self.__icon_theme = 'breeze'
                if not '[Icons]' in ini.content:
                    return self.__icon_theme

                if not 'Theme' in ini.content['[Icons]']:
                    return self.__icon_theme
                
                self.__icon_theme = ini.content['[Icons]']['Theme']
                return self.__icon_theme

        if self.__desktop_environment == 'mate':
            if self.__icon_theme:
                return self.__icon_theme

                gtk_icons = subprocess.getoutput(
                    'dconf read /org/mate/desktop/interface/icon-theme').strip(
                    "'")
                self.__icon_theme = gtk_icons if gtk_icons else None
                return self.__icon_theme

        if self.__desktop_environment == 'gnome':
            if self.__icon_theme:
                return self.__icon_theme

            gtk_icons = subprocess.getoutput(
                'gsettings get org.gnome.desktop.interface icon-theme').strip(
                "'")
            self.__icon_theme = gtk_icons if gtk_icons else None
            return self.__icon_theme

    def icon_source(
            self, icon: str | None, size: int = 16, dark: bool = None
            ) -> str:
        """..."""
        if not self.__icon_theme:
            self.icon_theme()

        if dark or dark is None and 'dark' in self.__icon_theme.lower():
            self.__icon_path = self.__path / 'static' / 'icons' / 'linux-dark'
        else:
            self.__icon_path = self.__path / 'static' / 'icons' / 'linux'

        if not icon:
            return str(self.__icon_path / 'empty.svg')

        if '/' in icon:
            if not Path(icon).exists():
                return str(self.__icon_path / 'empty.svg')
            return icon

        variant_theme = self.__icon_theme
        if dark and 'dark' not in self.__icon_theme.lower():
            variant_theme = self.icon_theme_dark_variant(self.__icon_theme)
        elif not dark and 'dark' in self.__icon_theme.lower():
            variant_theme = self.icon_theme_light_variant(self.__icon_theme)

        if variant_theme: self.__icon_theme = variant_theme 
        
        icon_path = IconTheme.getIconPath(
            iconname=icon,
            size=size,
            theme=self.__icon_theme,
            extensions=['png', 'svg', 'xpm'])

        """
        from PySide6.QtGui import QIcon
        icon = QIcon.fromTheme("document-save")

        Self impl:
        
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

        if icon_path:
            return icon_path

        icon = icon + '.svg'
        path = self.__icon_path / icon
        return str(path) if path.exists() else ''

    def icon_theme_variant(
            self, theme: str = None, dark: bool = True) -> str | None:
        """Dark or light variant icon theme"""
        if not theme:
            theme = self.icon_theme()

        new_theme = ''
        for path in self.__icon_theme_paths:
            for suffix in self.__dark_suffixes:
                
                if dark and 'dark' not in theme.lower():
                    if 'light' in theme.lower():
                        
                        for x in self.__light_suffixes:
                            theme = theme.replace(x, '')

                    if Path(path + theme + suffix).exists():
                        new_theme = theme + suffix

                elif not dark and 'dark' in theme.lower():
                    temp = theme.replace(suffix, '')
                    if Path(path+temp).exists() and 'dark' not in temp.lower():
                        new_theme = temp

        return new_theme if new_theme else None

    def icon_theme_dark_variant(self, theme: str = None) -> str | None:
        return self.icon_theme_variant(theme, True)

    def icon_theme_light_variant(self, theme: str = None) -> str | None:
        return self.icon_theme_variant(theme, False)
