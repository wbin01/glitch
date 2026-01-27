#!/usr/bin/env python3
import os
import platform
import subprocess
from pathlib import Path

from ..tools import color
from ..tools import DesktopFile


class Theme(object):
    """..."""
    def __init__(self, desktop: str) -> None:
        """..."""
        self.__desktop = desktop
        
        self.__accent = '#FF3C8CBD'
        self.__conf = self.__get_conf()
        self.__dark = False
        self.__theme = 'glitch'
        self.__set_themes()

    def __repr__(self) -> str:
        return self.__class__.__name__
    
    @property
    def accent(self) -> str:
        """..."""
        return self.__accent

    @accent.setter
    def accent(self, accent: str) -> None:
        self.__accent = accent

    @property
    def config(self) -> dict:
        """..."""
        return self.__conf

    @config.setter
    def config(self, config: dict) -> None:
        self.__conf = config

    @property
    def dark(self) -> bool:
        """..."""
        return self.__dark

    @dark.setter
    def dark(self, dark: str) -> None:
        self.__dark = dark

    @property
    def theme(self) -> str:
        """..."""
        return self.__theme

    @theme.setter
    def theme(self, theme: str) -> None:
        self.__theme = self.__theme

    def __get_conf(self) -> dict:
        path = None
        if self.__desktop == 'plasma':
            path = Path(os.environ['HOME']) / '.config' / 'kdeglobals'
        elif self.__desktop == 'lxqt':
            path = Path(os.environ['HOME']) / '.config' / 'lxqt' / 'lxqt.conf'

        if path and path.exists():
            return DesktopFile(path).content
        return {}
    
    def __set_themes(self) -> None:
        cinnamon_themes = {
            'aqua':   '#FF1F9EDE', 'blue':   '#FF0C75DE', 'brown': '#FFB7865E',
            'grey':   '#FF70737A', 'orange': '#FFFF7139', 'pink':  '#FFE54980',
            'purple': '#FF8C5DD9', 'red':    '#FFE82127', 'sand':  '#FFC5A07C',
            'teal':   '#FF199CA8'}

        if self.__desktop == 'cinnamon':
            # Theme
            cmd = subprocess.run(
                'gsettings get org.cinnamon.theme name',
                shell=True, capture_output=True, text=True)
            theme = cmd.stdout.strip().strip("'").strip('"')
            self.__theme = theme if theme else 'Mint-Y'

            # Accent
            theme_name_end = self.__theme.lower().split('-')[-1]
            accent = '#FF35A854'
            if theme_name_end in cinnamon_themes:
                accent = cinnamon_themes[theme_name_end]
            self.__accent = accent

            # Dark
            if 'dark' in self.__theme.lower():
                self.__dark = True

        elif self.__desktop == 'lxqt':
            # Theme
            self.__theme = 'Greybird'

            # Accent
            if ('[Palette]' in self.__conf and
                    'highlight_color' in self.__conf['[Palette]']):
                accent = self.__conf['[Palette]']['highlight_color']

                if accent: self.__accent = accent

            # Dark
            self.__dark = True
            if ('[Palette]' in self.__conf and
                    'window_color' in self.__theme.config['[Palette]']):
                bg = self.__theme.config['[Palette]']['window_color']
                
                if bg:self.__dark = color.is_dark(color.hex_to_rgba(app_bg))

        elif self.__desktop == 'pantheon':
            # Theme
            self.__theme = 'elementary'

            # Dark
            self.__dark = True

        elif self.__desktop == 'plasma':
            # Theme
            if ('[General]' in self.__conf and
                    'ColorScheme' in self.__conf['[General]']):
                theme = self.__conf['[General]']['ColorScheme']
                self.__theme = theme if theme else 'breeze'

            # Accent
            if ('[General]' in self.__conf and
                    'AccentColor' in self.__conf['[General]']):
                accent = color.plasma_color_to_hex(
                    self.__conf['[General]']['AccentColor'])

                if accent: self.__accent = accent

            # Dark
            if ('[Colors:Window]' in self.__conf and
                    'BackgroundNormal' in self.__conf['[Colors:Window]']):
                bg = color.plasma_color_to_hex(
                    self.__conf['[Colors:Window]']['BackgroundNormal'])

                if bg: self.__dark = color.is_dark(color.hex_to_rgba(bg))

        elif 'windows' in self.__desktop:
            # Theme
            self.__theme = 'windows'

            # Dark
            self.__dark = False

        else: # Glitch
            # Theme
            self.__theme = 'glitch'

            # Dark
            self.__dark = True
