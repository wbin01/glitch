#!/usr/bin/env python3
import os
import pathlib
import subprocess

from PySide6 import QtGui

from ..tools import color_converter as colr
from ..tools import DesktopFile


class Style(object):
    """Application style.
    
    Manages style information according to the platform.
    """

    def __init__(self, desktop_environment: str = 'plasma') -> None:
        self.__desktop = desktop_environment
        self.__style = None
        self.__conf = None
        self.__inactive_as_platform = False
        self.__accent_color = None

        self.__path = pathlib.Path(__file__).parent.parent
        self.__icon_path = str(self.__path) + '/static/control_button/plasma/'
        self.__plasma_close_button_with_circle = False
        self.__symbolic = ''
        self.__app_frame_bg = None
        self.__cinnamon_theme = None

    @property
    def accent_color(self) -> str:
        """..."""
        if not self.__conf:
            self.__conf = self.__get_sys_conf()

        if not self.__accent_color:
            if self.__desktop == 'plasma':
                self.__accent_color = self.__color_to_hex(
                    self.__conf['[General]']['AccentColor'], '#FF3C8CBD')

            elif self.__desktop == 'cinnamon':
                if not self.__cinnamon_theme:
                    self.__set_cinnamon_theme()

        return self.__accent_color

    @accent_color.setter
    def accent_color(self, accent_color: str) -> None:
        self.__accent_color = self.__accent_color

    @property
    def style(self) -> dict:
        """..."""
        if self.__style:
            return self.__style

        if not self.__conf:
            self.__conf = self.__get_sys_conf()

        if not self.__app_frame_bg:
            self.__set_styles()

        self.__style = {
            '[Button]': {
                'background_color': self.__button_bg,
                'border_color': self.__button_bd,
                'font_color': self.__button_fg,
                'icon_opacity': self.__button_io,
                'border_width': '1',
                'border_radius': self.__button_rd,
                },
            '[Button:inactive]': {
                'background_color': self.__button_in_bg,
                'border_color': self.__button_in_bd,
                'font_color': self.__button_in_fg,
                'icon_opacity': self.__button_in_io,
                },
            '[Button:hover]': {
                'background_color': self.__button_hv_bg,
                'border_color': self.__button_hv_bd,
                'font_color': self.__button_hv_fg,
                # 'icon_opacity': self.__button_hv_io,
                },
            '[Button:clicked]': {
                'background_color': self.__button_ck_bg,
                'border_color': self.__button_ck_bd,
                'font_color': self.__button_ck_fg,
                # 'icon_opacity': self.__button_ck_io,
                },
            '[Button:checked]': {
                'background_color': self.__button_ch_bg,
                'border_color': self.__button_ch_bd,
                'font_color': self.__button_ch_fg,
                # 'icon_opacity': self.__button_ch_io,
                },
            '[Button:checked:inactive]': {
                'background_color': self.__button_ch_in_bg,
                'border_color': self.__button_ch_in_bd,
                'font_color': self.__button_ch_in_fg,
                'icon_opacity': self.__button_ch_in_io,
                },
            '[Button:checked:hover]': {
                'background_color': self.__button_ch_hv_bg,
                'border_color': self.__button_ch_hv_bd,
                'font_color': self.__button_ch_hv_fg,
                # 'icon_opacity': self.__button_ch_hv_io,
                },
            '[CloseButton]': {
                'background_color': self.__close_button_bg,
                'border_color': self.__close_button_bd,
                'font_color': self.__close_button_fg,
                'icon_opacity': self.__close_button_io,
                'icon': self.__close_button_i,
                'border_width': '0',
                'border_radius': self.__close_button_rd,
                },
            '[CloseButton:inactive]': {
                'background_color': self.__close_button_in_bg,
                'border_color': self.__close_button_in_bd,
                'font_color': self.__close_button_in_fg,
                'icon_opacity': self.__close_button_in_io,
                'icon': self.__close_button_in_i,
                },
            '[CloseButton:hover]': {
                'background_color': self.__close_button_hv_bg,
                'border_color': self.__close_button_hv_bd,
                'font_color': self.__close_button_hv_fg,
                'icon_opacity': self.__close_button_hv_io,
                'icon': self.__close_button_hv_i,
                },
            '[CloseButton:clicked]': {
                'background_color': self.__close_button_ck_bg,
                'border_color': self.__close_button_ck_bd,
                'font_color': self.__close_button_ck_fg,
                'icon_opacity': self.__close_button_ck_io,
                'icon': self.__close_button_ck_i,
                },
            '[Frame]': {
                'background_color': self.__frame_bg,
                'border_color': self.__frame_bd,
                'border_radius': self.__frame_rd,
                },
            '[Frame:inactive]': {
                'background_color': self.__frame_in_bg,
                'border_color': self.__frame_in_bd,
                },
            '[FullButton]': {
                'background_color': self.__full_button_bg,
                'border_color': self.__full_button_bd,
                'font_color': self.__full_button_fg,
                'icon_opacity': self.__full_button_io,
                'icon': self.__full_button_i,
                'restore_icon': self.__full_button_ir,
                'border_width': '0',
                'border_radius': self.__full_button_rd,
                },
            '[FullButton:inactive]': {
                'background_color': self.__full_button_in_bg,
                'border_color': self.__full_button_in_bd,
                'font_color': self.__full_button_in_fg,
                'icon_opacity': self.__full_button_in_io,
                'icon': self.__full_button_in_i,
                'restore_icon': self.__full_button_in_ir,
                },
            '[FullButton:hover]': {
                'background_color': self.__full_button_hv_bg,
                'border_color': self.__full_button_hv_bd,
                'font_color': self.__full_button_hv_fg,
                'icon_opacity': self.__full_button_hv_io,
                'icon': self.__full_button_hv_i,
                'restore_icon': self.__full_button_hv_ir,
                },
            '[FullButton:clicked]': {
                'background_color': self.__full_button_ck_bg,
                'border_color': self.__full_button_ck_bd,
                'font_color': self.__full_button_ck_fg,
                'icon_opacity': self.__full_button_ck_io,
                'icon': self.__full_button_ck_i,
                'restore_icon': self.__full_button_ck_ir,
                },
            '[Label]': {
                'font_color': self.__label_fg,
                'background_color': self.__label_bg,
                },
            '[Label:inactive]': {
                'font_color': self.__label_in_fg,
                'background_color': self.__label_in_bg,
                },
            '[MainFrame]': {
                'background_color': self.__app_frame_bg,
                'border_color': self.__app_frame_bd,
                'border_radius': self.__app_frame_rd,
                },
            '[MainFrame:inactive]': {
                'background_color': self.__app_frame_in_bg,
                'border_color': self.__app_frame_in_bd,
                },
            '[MaxButton]': {
                'background_color': self.__max_button_bg,
                'border_color': self.__max_button_bd,
                'font_color': self.__max_button_fg,
                'icon_opacity': self.__max_button_io,
                'icon': self.__max_button_i,
                'restore_icon': self.__max_button_ir,
                'border_width': '0',
                'border_radius': self.__max_button_rd,
                },
            '[MaxButton:inactive]': {
                'background_color': self.__max_button_in_bg,
                'border_color': self.__max_button_in_bd,
                'font_color': self.__max_button_in_fg,
                'icon_opacity': self.__max_button_in_io,
                'icon': self.__max_button_in_i,
                'restore_icon': self.__max_button_in_ir,
                },
            '[MaxButton:hover]': {
                'background_color': self.__max_button_hv_bg,
                'border_color': self.__max_button_hv_bd,
                'font_color': self.__max_button_hv_fg,
                'icon_opacity': self.__max_button_hv_io,
                'icon': self.__max_button_hv_i,
                'restore_icon': self.__max_button_hv_ir,
                },
            '[MaxButton:clicked]': {
                'background_color': self.__max_button_ck_bg,
                'border_color': self.__max_button_ck_bd,
                'font_color': self.__max_button_ck_fg,
                'icon_opacity': self.__max_button_ck_io,
                'icon': self.__max_button_ck_i,
                'restore_icon': self.__max_button_ck_ir,
                },
            '[MinButton]': {
                'background_color': self.__min_button_bg,
                'border_color': self.__min_button_bd,
                'font_color': self.__min_button_fg,
                'icon_opacity': self.__min_button_io,
                'icon': self.__min_button_i,
                'border_width': '0',
                'border_radius': self.__min_button_rd,
                },
            '[MinButton:inactive]': {
                'background_color': self.__min_button_in_bg,
                'border_color': self.__min_button_in_bd,
                'font_color': self.__min_button_in_fg,
                'icon_opacity': self.__min_button_in_io,
                'icon': self.__min_button_in_i,
                },
            '[MinButton:hover]': {
                'background_color': self.__min_button_hv_bg,
                'border_color': self.__min_button_hv_bd,
                'font_color': self.__min_button_hv_fg,
                'icon_opacity': self.__min_button_hv_io,
                'icon': self.__min_button_hv_i,
                },
            '[MinButton:clicked]': {
                'background_color': self.__min_button_ck_bg,
                'border_color': self.__min_button_ck_bd,
                'font_color': self.__min_button_ck_fg,
                'icon_opacity': self.__min_button_ck_io,
                'icon': self.__min_button_ck_i,
                },
            '[Panel]': {
                'background_color': self.__panel_bg,
                'border_color': self.__panel_bd,
                'border_radius': self.__panel_rd,
                },
            '[Panel:inactive]': {
                'background_color': self.__panel_in_bg,
                'border_color': self.__panel_in_bd,
                # 'border_radius': '10',
                },
            '[ToolButton]': {
                'background_color': self.__tool_button_bg,
                'border_color': self.__tool_button_bd,
                'icon_opacity': self.__tool_button_io,
                'border_width': '1',
                'border_radius': self.__tool_button_rd,
                },
            '[ToolButton:inactive]': {
                'background_color': self.__tool_button_in_bg,
                'border_color': self.__tool_button_in_bd,
                'icon_opacity': self.__tool_button_in_io,
                },
            '[ToolButton:hover]': {
                'background_color': self.__tool_button_hv_bg,
                'border_color': self.__tool_button_hv_bd,
                'icon_opacity': self.__tool_button_hv_io,
                },
            '[ToolButton:clicked]': {
                'background_color': self.__tool_button_ck_bg,
                'border_color': self.__tool_button_ck_bd,
                'icon_opacity': self.__tool_button_ck_io,
                },
            '[ToolButton:checked]': {
                'background_color': self.__tool_button_ch_bg,
                'border_color': self.__tool_button_ch_bd,
                'icon_opacity': self.__tool_button_ch_io,
                },
            '[ToolButton:checked:inactive]': {
                'background_color': self.__tool_button_ch_in_bg,
                'border_color': self.__tool_button_ch_in_bd,
                'icon_opacity': self.__tool_button_ch_in_io,
                },
            '[ToolButton:checked:hover]': {
                'background_color': self.__tool_button_ch_hv_bg,
                'border_color': self.__tool_button_ch_hv_bd,
                'icon_opacity': self.__tool_button_ch_hv_io,
                },
            }
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    def print(self) -> None:
        for key, value in self.style().items():
            print(key)
            for k, v in value.items():
                print(f'{k}: {v}')
            print()

    def __color_to_hex(self, color, alt_color) -> str:
        color = color.split(',')
        len_color = len(color)

        if self.__desktop == 'plasma':
            if len_color == 3:
                color = int(color[0]), int(color[1]), int(color[2]), 255
            else:
                color = int(
                    color[0]), int(color[1]), int(color[2]), int(color[3])
            return colr.rgba_to_hex(color)
        return alt_color

    def __get_sys_conf(self) -> dict:
        conf_name = 'kdeglobals'
        conf_file = pathlib.Path(os.environ['HOME']) / '.config' / conf_name

        ini = {}
        if conf_file.exists():
            ini = DesktopFile(conf_file).content
        return ini

    def __set_styles(self) -> None:
        # self.__inactive_as_platform = True

        # Needs to have this order. The settings below need the settings above.
        if self.__desktop == 'cinnamon':
            self.__app_frame_style_cinnamon()
            self.__frame_style_cinnamon()
            self.__label_style_cinnamon()
            self.__button_style_cinnamon()

            self.__tool_button_style_cinnamon()
            self.__close_button_style_cinnamon()
            self.__full_button_style_cinnamon()
            self.__max_button_style_cinnamon()
            self.__min_button_style_cinnamon()
            self.__panel_style_cinnamon()

        elif self.__desktop == 'plasma':
            self.__app_frame_style_plasma()
            self.__frame_style_plasma()
            self.__label_style_plasma()
            self.__button_style_plasma()

            self.__tool_button_style_plasma()
            self.__close_button_style_plasma()
            self.__full_button_style_plasma()
            self.__max_button_style_plasma()
            self.__min_button_style_plasma()
            self.__panel_style_plasma()

    def __app_frame_style_cinnamon(self) -> None:
        if not self.__cinnamon_theme:
            self.__set_cinnamon_theme()

        if 'dark' in self.__cinnamon_theme.lower():
            self.__app_frame_fg = '#FFCCCCCC'
            self.__app_frame_bg = '#FF222226'
        else:
            self.__app_frame_fg = '#FF333333'
            self.__app_frame_bg = '#FFEBEBED'

        self.__app_frame_is_dark = colr.is_dark(
            colr.hex_to_rgba(self.__app_frame_bg))

        self.__app_frame_bd = self.__app_frame_bg
        if self.__app_frame_is_dark:
            self.__app_frame_bd = '#FF111111'

        self.__app_frame_rd = '8, 8, 0, 0'
        self.__app_frame_io = '1.0'

        # Inactive
        if self.__inactive_as_platform:
            # [Colors:Header][Inactive]][BackgroundNormal]
            self.__app_frame_in_fg = self.__app_frame_fg
            self.__app_frame_in_bg = self.__app_frame_bg
            self.__app_frame_in_io = self.__app_frame_io
            self.__app_frame_in_bd = self.__app_frame_bd
        else:
            self.__app_frame_in_fg = '#50' + self.__app_frame_fg[3:]
            self.__app_frame_in_bg = colr.darken_hex(self.__app_frame_bg, 4)
            self.__app_frame_in_io = '0.2'

            self.__app_frame_in_bd = self.__app_frame_in_bg
            if self.__app_frame_is_dark:
                self.__app_frame_in_bd = colr.lighten_hex(
                    self.__app_frame_in_bg, 5)

    def __app_frame_style_plasma(self) -> None:
        self.__app_frame_fg = self.__color_to_hex(
            self.__conf['[Colors:Window]']['ForegroundNormal'], '#FFFFFF')
        
        self.__app_frame_bg = self.__color_to_hex(  # Alt 282828
            self.__conf['[Colors:Window]']['BackgroundNormal'], '#2A2A2A')

        self.__app_frame_is_dark = colr.is_dark(
            colr.hex_to_rgba(self.__app_frame_bg))

        self.__app_frame_bd = self.__app_frame_bg
        if self.__app_frame_is_dark:
            self.__app_frame_bd = colr.lighten_hex(self.__app_frame_bg, 15)

        self.__app_frame_rd = '6, 6, 6, 6'
        self.__app_frame_io = '1.0'

        # Inactive
        if self.__inactive_as_platform:
            # [Colors:Header][Inactive]][BackgroundNormal]
            self.__app_frame_in_fg = self.__app_frame_fg
            self.__app_frame_in_bg = self.__app_frame_bg
            self.__app_frame_in_io = self.__app_frame_io
            self.__app_frame_in_bd = self.__app_frame_bd
        else:
            self.__app_frame_in_fg = '#50' + self.__app_frame_fg[3:]
            self.__app_frame_in_bg = colr.darken_hex(self.__app_frame_bg, 4)
            self.__app_frame_in_io = '0.2'

            self.__app_frame_in_bd = self.__app_frame_in_bg
            if self.__app_frame_is_dark:
                self.__app_frame_in_bd = colr.lighten_hex(
                    self.__app_frame_in_bg, 5)

    def __frame_style_cinnamon(self) -> None:
        self.__frame_is_dark = self.__app_frame_is_dark
        self.__frame_fg = self.__app_frame_fg
        self.__frame_bg = self.__app_frame_bg
        self.__frame_bd = self.__app_frame_bd
        self.__frame_rd = (self.__app_frame_rd.split(',')[0] + ',') * 4
        self.__frame_in_fg = self.__app_frame_in_fg
        self.__frame_in_bg = self.__app_frame_in_bg
        self.__frame_in_bd = self.__app_frame_in_bd

    def __frame_style_plasma(self) -> None:
        self.__frame_is_dark = self.__app_frame_is_dark
        self.__frame_fg = self.__app_frame_fg
        self.__frame_bg = self.__app_frame_bg
        self.__frame_bd = self.__app_frame_bd
        self.__frame_rd = (self.__app_frame_rd.split(',')[0] + ',') * 4
        self.__frame_in_fg = self.__app_frame_in_fg
        self.__frame_in_bg = self.__app_frame_in_bg
        self.__frame_in_bd = self.__app_frame_in_bd

    def __label_style_cinnamon(self) -> None:
        self.__label_fg = self.__app_frame_fg
        self.__label_bg = self.__app_frame_bg
        self.__label_in_fg = self.__app_frame_in_fg
        self.__label_in_bg = self.__app_frame_in_bg

    def __label_style_plasma(self) -> None:
        self.__label_fg = self.__app_frame_fg
        self.__label_bg = self.__app_frame_bg
        self.__label_in_fg = self.__app_frame_in_fg
        self.__label_in_bg = self.__app_frame_in_bg

    def __button_style_cinnamon(self) -> None:
        self.__button_fg = self.__app_frame_fg
        
        if self.__app_frame_is_dark:
            self.__button_bg = colr.lighten_hex(self.__app_frame_bg, 3)
        else:
            self.__button_bg = self.__app_frame_bg

        if self.__app_frame_is_dark:
            self.__button_bd = '#FF181818'
        else:
            self.__button_bd = colr.darken_hex(self.__button_bg, 35)
        
        self.__button_rd = '6'
        self.__button_io = self.__app_frame_io

        # Inactive
        self.__button_in_fg = self.__app_frame_in_fg

        if self.__inactive_as_platform:
            self.__button_in_bg = self.__button_bg
            self.__button_in_bd = self.__button_bd
        else:
            self.__button_in_bg = '#AA' + self.__button_bg[3:]
            self.__button_in_bd = '#80' + self.__button_bd[3:]
        
        self.__button_in_io = self.__app_frame_in_io

        # Hover
        self.__button_hv_fg = self.__button_fg
        self.__button_hv_bg = self.__button_bg
        self.__button_hv_bd = self.__button_bd

        if 'dark' in self.__cinnamon_theme.lower():
            self.__button_hv_bg = colr.lighten_hex(self.__button_bg, 5)
        else:
            self.__button_hv_bg = colr.darken_hex(self.__button_bg, 4)

        self.__button_hv_io = self.__button_io

        # Clicked
        self.__button_ck_fg = self.__button_fg
        self.__button_ck_bg = '#33' + self.__button_hv_bd[3:]
        self.__button_ck_bd = self.__button_hv_bd
        self.__button_ck_io = self.__button_io

        # Checked
        self.__button_ch_fg = self.__button_fg
        self.__button_ch_bg = '#AA' + self.__button_bd[3:]
        self.__button_ch_bd = self.__button_bd
        self.__button_ch_io = self.__button_io

        # Checked inactive
        self.__button_ch_in_fg = self.__button_in_fg

        if self.__inactive_as_platform:
            self.__button_ch_in_bg = self.__button_ch_bg
        else:
            self.__button_ch_in_bg = '#33' + self.__button_ch_bg[3:]

        self.__button_ch_in_bd = self.__button_in_bd
        self.__button_ch_in_io = self.__button_in_io
        
        # Checked hover
        self.__button_ch_hv_fg = self.__button_ch_fg
        self.__button_ch_hv_bg = self.__button_ch_bg
        self.__button_ch_hv_bd = self.__button_hv_bd
        self.__button_ch_hv_io = self.__button_ch_io

    def __button_style_plasma(self) -> None:
        self.__button_fg = self.__app_frame_fg
        self.__button_bg = self.__color_to_hex(
            self.__conf['[Colors:Button]']['BackgroundNormal'], '#33333333')

        if self.__app_frame_is_dark:
            self.__button_bd = colr.lighten_hex(self.__button_bg, 35)
        else:
            self.__button_bd = colr.darken_hex(self.__button_bg, 35)
        
        self.__button_rd = '6'
        self.__button_io = self.__app_frame_io

        # Inactive
        self.__button_in_fg = self.__app_frame_in_fg

        if self.__inactive_as_platform:
            self.__button_in_bg = self.__button_bg
            self.__button_in_bd = self.__button_bd
        else:
            self.__button_in_bg = '#AA' + self.__button_bg[3:]  # self.__app_frame_in_bg
            self.__button_in_bd = '#80' + self.__button_bd[3:]
        
        self.__button_in_io = self.__app_frame_in_io

        # Hover
        self.__button_hv_fg = self.__button_fg
        self.__button_hv_bg = self.__button_bg

        self.__button_hv_bd = '#99' + self.__color_to_hex(
            self.__conf['[Colors:Button]']['DecorationHover'],'#3C8CBD')[3:]
        self.__button_hv_io = self.__button_io

        # Clicked
        self.__button_ck_fg = self.__button_fg
        self.__button_ck_bg = '#33' + self.__button_hv_bd[3:]
        self.__button_ck_bd = self.__button_hv_bd
        self.__button_ck_io = self.__button_io

        # Checked
        self.__button_ch_fg = self.__button_fg
        self.__button_ch_bg = '#AA' + self.__button_bd[3:]
        self.__button_ch_bd = self.__button_bd
        self.__button_ch_io = self.__button_io

        # Checked inactive
        self.__button_ch_in_fg = self.__button_in_fg

        if self.__inactive_as_platform:
            self.__button_ch_in_bg = self.__button_ch_bg
        else:
            self.__button_ch_in_bg = '#33' + self.__button_ch_bg[3:]

        self.__button_ch_in_bd = self.__button_in_bd
        self.__button_ch_in_io = self.__button_in_io
        
        # Checked hover
        self.__button_ch_hv_fg = self.__button_ch_fg
        self.__button_ch_hv_bg = self.__button_ch_bg
        self.__button_ch_hv_bd = self.__button_hv_bd
        self.__button_ch_hv_io = self.__button_ch_io

    def __tool_button_style_cinnamon(self) -> None:
        self.__tool_button_bg = self.__app_frame_bg
        self.__tool_button_bd = self.__app_frame_bg
        self.__tool_button_io = self.__button_io
        self.__tool_button_rd = self.__button_rd

        # Inactive
        self.__tool_button_in_bg = '#00000000'  # self.__app_frame_in_bg
        self.__tool_button_in_bd = '#00000000'  # self.__app_frame_in_bg
        self.__tool_button_in_io = self.__button_in_io
        
        # Hover
        self.__tool_button_hv_bg = self.__tool_button_bg
        self.__tool_button_hv_bd = self.__button_hv_bd
        self.__tool_button_hv_io = self.__tool_button_io

        # Clicked
        self.__tool_button_ck_bg = self.__button_ck_bg
        self.__tool_button_ck_bd = self.__button_ck_bd
        self.__tool_button_ck_io = self.__button_ck_io

        # Checked
        self.__tool_button_ch_bg = '#88' + self.__button_ch_bg[3:]
        self.__tool_button_ch_bd = self.__button_ch_bd
        self.__tool_button_ch_io = self.__button_ch_io

        # Checked inactive
        if self.__inactive_as_platform:
            self.__tool_button_ch_in_bg = self.__tool_button_ch_bg
            self.__tool_button_ch_in_bd = self.__tool_button_ch_bd
        else:
            self.__tool_button_ch_in_bg = '#33' + self.__tool_button_ch_bg[3:]
            self.__tool_button_ch_in_bd = '#33' + self.__tool_button_ch_bd[3:]

        self.__tool_button_ch_in_io = self.__tool_button_in_io

        # Checked hover
        self.__tool_button_ch_hv_bg = self.__tool_button_ch_bg
        self.__tool_button_ch_hv_bd = self.__tool_button_hv_bd
        self.__tool_button_ch_hv_io = self.__tool_button_ch_io

    def __tool_button_style_plasma(self) -> None:
        self.__tool_button_bg = self.__app_frame_bg
        self.__tool_button_bd = self.__app_frame_bg
        self.__tool_button_io = self.__button_io
        self.__tool_button_rd = self.__button_rd

        # Inactive
        self.__tool_button_in_bg = '#00000000'  # self.__app_frame_in_bg
        self.__tool_button_in_bd = '#00000000'  # self.__app_frame_in_bg
        self.__tool_button_in_io = self.__button_in_io
        
        # Hover
        self.__tool_button_hv_bg = self.__tool_button_bg
        self.__tool_button_hv_bd = self.__button_hv_bd
        self.__tool_button_hv_io = self.__tool_button_io

        # Clicked
        self.__tool_button_ck_bg = self.__button_ck_bg
        self.__tool_button_ck_bd = self.__button_ck_bd
        self.__tool_button_ck_io = self.__button_ck_io

        # Checked
        self.__tool_button_ch_bg = '#88' + self.__button_ch_bg[3:]
        self.__tool_button_ch_bd = self.__button_ch_bd
        self.__tool_button_ch_io = self.__button_ch_io

        # Checked inactive
        if self.__inactive_as_platform:
            self.__tool_button_ch_in_bg = self.__tool_button_ch_bg
            self.__tool_button_ch_in_bd = self.__tool_button_ch_bd
        else:
            self.__tool_button_ch_in_bg = '#33' + self.__tool_button_ch_bg[3:]
            self.__tool_button_ch_in_bd = '#33' + self.__tool_button_ch_bd[3:]

        self.__tool_button_ch_in_io = self.__tool_button_in_io

        # Checked hover
        self.__tool_button_ch_hv_bg = self.__tool_button_ch_bg
        self.__tool_button_ch_hv_bd = self.__tool_button_hv_bd
        self.__tool_button_ch_hv_io = self.__tool_button_ch_io

    def __close_button_style_cinnamon(self) -> None:
        icon = 'window-close'
        ico = icon if self.__plasma_close_button_with_circle else icon + '-b'
        self.__symbolic = '-symbolic' if self.__app_frame_is_dark else ''

        self.__close_button_bg = '#00000000'
        self.__close_button_bd = '#00000000'
        self.__close_button_fg = self.__app_frame_fg
        self.__close_button_io = self.__button_io
        self.__close_button_i = (
            self.__icon_path + ico + self.__symbolic + '.svg')
        self.__close_button_rd = self.__tool_button_rd

        # Inactive
        self.__close_button_in_bg = self.__app_frame_in_bg
        self.__close_button_in_bd = self.__app_frame_in_bg
        self.__close_button_in_fg = self.__app_frame_in_fg
        self.__close_button_in_io = self.__button_in_io
        self.__close_button_in_i = (
            self.__icon_path + ico + '-inactive' + self.__symbolic + '.svg')

        # Hover
        self.__close_button_hv_bg = self.__app_frame_bg
        self.__close_button_hv_bd = self.__app_frame_bg
        self.__close_button_hv_fg = self.__app_frame_fg
        self.__close_button_hv_io = self.__button_hv_io
        self.__close_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__close_button_ck_bg = self.__app_frame_bg
        self.__close_button_ck_bd = self.__app_frame_bg
        self.__close_button_ck_fg = self.__app_frame_fg
        self.__close_button_ck_io = self.__button_ck_io
        self.__close_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __close_button_style_plasma(self) -> None:
        icon = 'window-close'
        ico = icon if self.__plasma_close_button_with_circle else icon + '-b'
        self.__symbolic = '-symbolic' if self.__app_frame_is_dark else ''

        self.__close_button_bg = '#00000000'
        self.__close_button_bd = '#00000000'
        self.__close_button_fg = self.__app_frame_fg
        self.__close_button_io = self.__button_io
        self.__close_button_i = (
            self.__icon_path + ico + self.__symbolic + '.svg')
        self.__close_button_rd = self.__tool_button_rd

        # Inactive
        self.__close_button_in_bg = self.__app_frame_in_bg
        self.__close_button_in_bd = self.__app_frame_in_bg
        self.__close_button_in_fg = self.__app_frame_in_fg
        self.__close_button_in_io = self.__button_in_io
        self.__close_button_in_i = (
            self.__icon_path + ico + '-inactive' + self.__symbolic + '.svg')

        # Hover
        self.__close_button_hv_bg = self.__app_frame_bg
        self.__close_button_hv_bd = self.__app_frame_bg
        self.__close_button_hv_fg = self.__app_frame_fg
        self.__close_button_hv_io = self.__button_hv_io
        self.__close_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__close_button_ck_bg = self.__app_frame_bg
        self.__close_button_ck_bd = self.__app_frame_bg
        self.__close_button_ck_fg = self.__app_frame_fg
        self.__close_button_ck_io = self.__button_ck_io
        self.__close_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __full_button_style_cinnamon(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__full_button_bg = self.__close_button_bg
        self.__full_button_bd = self.__close_button_bd
        self.__full_button_fg = self.__close_button_fg
        self.__full_button_io = self.__close_button_io
        self.__full_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__full_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__full_button_rd = self.__tool_button_rd

        # Inactive
        self.__full_button_in_bg = self.__close_button_in_bg
        self.__full_button_in_bd = self.__close_button_in_bd
        self.__full_button_in_fg = self.__close_button_in_fg
        self.__full_button_in_io = self.__close_button_in_io
        self.__full_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__full_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic +'.svg')
        
        # Hover
        self.__full_button_hv_bg = self.__close_button_hv_bg
        self.__full_button_hv_bd = self.__close_button_hv_bd
        self.__full_button_hv_fg = self.__close_button_hv_fg
        self.__full_button_hv_io = self.__close_button_hv_io
        self.__full_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__full_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')
        
        # Clicked
        self.__full_button_ck_bg = self.__close_button_ck_bg
        self.__full_button_ck_bd = self.__close_button_ck_bd
        self.__full_button_ck_fg = self.__close_button_ck_fg
        self.__full_button_ck_io = self.__close_button_ck_io
        self.__full_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__full_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __full_button_style_plasma(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__full_button_bg = self.__close_button_bg
        self.__full_button_bd = self.__close_button_bd
        self.__full_button_fg = self.__close_button_fg
        self.__full_button_io = self.__close_button_io
        self.__full_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__full_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__full_button_rd = self.__tool_button_rd

        # Inactive
        self.__full_button_in_bg = self.__close_button_in_bg
        self.__full_button_in_bd = self.__close_button_in_bd
        self.__full_button_in_fg = self.__close_button_in_fg
        self.__full_button_in_io = self.__close_button_in_io
        self.__full_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__full_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic +'.svg')
        
        # Hover
        self.__full_button_hv_bg = self.__close_button_hv_bg
        self.__full_button_hv_bd = self.__close_button_hv_bd
        self.__full_button_hv_fg = self.__close_button_hv_fg
        self.__full_button_hv_io = self.__close_button_hv_io
        self.__full_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__full_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')
        
        # Clicked
        self.__full_button_ck_bg = self.__close_button_ck_bg
        self.__full_button_ck_bd = self.__close_button_ck_bd
        self.__full_button_ck_fg = self.__close_button_ck_fg
        self.__full_button_ck_io = self.__close_button_ck_io
        self.__full_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__full_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __max_button_style_cinnamon(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__max_button_bg = self.__close_button_bg
        self.__max_button_bd = self.__close_button_bd
        self.__max_button_fg = self.__close_button_fg
        self.__max_button_io = self.__close_button_io
        self.__max_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__max_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__max_button_rd = self.__tool_button_rd

        # Inactive
        self.__max_button_in_bg = self.__close_button_in_bg
        self.__max_button_in_bd = self.__close_button_in_bd
        self.__max_button_in_fg = self.__close_button_in_fg
        self.__max_button_in_io = self.__close_button_in_io
        self.__max_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__max_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic +'.svg')
        
        # Hover
        self.__max_button_hv_bg = self.__close_button_hv_bg
        self.__max_button_hv_bd = self.__close_button_hv_bd
        self.__max_button_hv_fg = self.__close_button_hv_fg
        self.__max_button_hv_io = self.__close_button_hv_io
        self.__max_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__max_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__max_button_ck_bg = self.__close_button_ck_bg
        self.__max_button_ck_bd = self.__close_button_ck_bd
        self.__max_button_ck_fg = self.__close_button_ck_fg
        self.__max_button_ck_io = self.__close_button_ck_io
        self.__max_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__max_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __max_button_style_plasma(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__max_button_bg = self.__close_button_bg
        self.__max_button_bd = self.__close_button_bd
        self.__max_button_fg = self.__close_button_fg
        self.__max_button_io = self.__close_button_io
        self.__max_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__max_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__max_button_rd = self.__tool_button_rd

        # Inactive
        self.__max_button_in_bg = self.__close_button_in_bg
        self.__max_button_in_bd = self.__close_button_in_bd
        self.__max_button_in_fg = self.__close_button_in_fg
        self.__max_button_in_io = self.__close_button_in_io
        self.__max_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__max_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic +'.svg')
        
        # Hover
        self.__max_button_hv_bg = self.__close_button_hv_bg
        self.__max_button_hv_bd = self.__close_button_hv_bd
        self.__max_button_hv_fg = self.__close_button_hv_fg
        self.__max_button_hv_io = self.__close_button_hv_io
        self.__max_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__max_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__max_button_ck_bg = self.__close_button_ck_bg
        self.__max_button_ck_bd = self.__close_button_ck_bd
        self.__max_button_ck_fg = self.__close_button_ck_fg
        self.__max_button_ck_io = self.__close_button_ck_io
        self.__max_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__max_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __min_button_style_cinnamon(self) -> None:
        icon = 'go-down'
        self.__min_button_bg = self.__close_button_bg
        self.__min_button_bd = self.__close_button_bd
        self.__min_button_fg = self.__close_button_fg
        self.__min_button_io = self.__close_button_io
        self.__min_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__min_button_rd = self.__tool_button_rd

        # Inactive
        self.__min_button_in_bg = self.__close_button_in_bg
        self.__min_button_in_bd = self.__close_button_in_bd
        self.__min_button_in_fg = self.__close_button_in_fg
        self.__min_button_in_io = self.__close_button_in_io
        self.__min_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')

        # Hover
        self.__min_button_hv_bg = self.__close_button_hv_bg
        self.__min_button_hv_bd = self.__close_button_hv_bd
        self.__min_button_hv_fg = self.__close_button_hv_fg
        self.__min_button_hv_io = self.__close_button_hv_io
        self.__min_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__min_button_ck_bg = self.__close_button_ck_bg
        self.__min_button_ck_bd = self.__close_button_ck_bd
        self.__min_button_ck_fg = self.__close_button_ck_fg
        self.__min_button_ck_io = self.__close_button_ck_io
        self.__min_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __min_button_style_plasma(self) -> None:
        icon = 'go-down'
        self.__min_button_bg = self.__close_button_bg
        self.__min_button_bd = self.__close_button_bd
        self.__min_button_fg = self.__close_button_fg
        self.__min_button_io = self.__close_button_io
        self.__min_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__min_button_rd = self.__tool_button_rd

        # Inactive
        self.__min_button_in_bg = self.__close_button_in_bg
        self.__min_button_in_bd = self.__close_button_in_bd
        self.__min_button_in_fg = self.__close_button_in_fg
        self.__min_button_in_io = self.__close_button_in_io
        self.__min_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')

        # Hover
        self.__min_button_hv_bg = self.__close_button_hv_bg
        self.__min_button_hv_bd = self.__close_button_hv_bd
        self.__min_button_hv_fg = self.__close_button_hv_fg
        self.__min_button_hv_io = self.__close_button_hv_io
        self.__min_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')

        # Clicked
        self.__min_button_ck_bg = self.__close_button_ck_bg
        self.__min_button_ck_bd = self.__close_button_ck_bd
        self.__min_button_ck_fg = self.__close_button_ck_fg
        self.__min_button_ck_io = self.__close_button_ck_io
        self.__min_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __panel_style_cinnamon(self) -> None:
        if self.__app_frame_is_dark:
            self.__panel_bg = '#FA' + colr.darken_hex(self.__app_frame_bg, 5)[3:]
        else:
            self.__panel_bg = '#FA' + colr.darken_hex(self.__app_frame_bg, 10)[3:]

        self.__panel_bd = self.__panel_bg
        self.__panel_rd = self.__app_frame_rd

        # Inactive
        self.__panel_in_bg = colr.darken_hex(self.__app_frame_in_bg, 5)
        self.__panel_in_bd = self.__panel_in_bg

    def __panel_style_plasma(self) -> None:
        self.__panel_bg = '#FA' + colr.darken_hex(self.__app_frame_bg, 5)[3:]
        self.__panel_bd = self.__panel_bg
        self.__panel_rd = self.__app_frame_rd

        # Inactive
        self.__panel_in_bg = colr.darken_hex(self.__app_frame_in_bg, 5)
        self.__panel_in_bd = self.__panel_in_bg

    def __set_cinnamon_theme(self):
        if self.__cinnamon_theme:
            return self.__cinnamon_theme

        cmd = subprocess.run(
            'gsettings get org.cinnamon.theme name',
            shell=True, capture_output=True, text=True)
        self.__cinnamon_theme = cmd.stdout.strip().strip("'").strip('"')
        themes = {
            'aqua':   '#FF6CADD0', 'blue':   '#FF5986C9', 'brown': '#FFB7865E',
            'grey':   '#FF9D9D9D', 'orange': '#FFDB9D61', 'pink':  '#FFC76199',
            'purple': '#FF8C6EC9', 'red':    '#FFC15b58', 'sand':  '#FFC8AC69',
            'teal':   '#FF5AAA9A'}

        theme_name_end = self.__cinnamon_theme.lower().split('-')[-1]
        if theme_name_end in ['l', 'x', 'y']:
            self.__accent_color = '#FF9AB87C'
        elif theme_name_end == 'dark':
            self.__accent_color = '#FF8FA876'
        elif theme_name_end == 'darker':
            self.__accent_color = '#FF9AB87C'
        elif theme_name_end in themes:
            self.__accent_color = themes[theme_name_end]
        else:
            self.__accent_color = '#FF9AB87C'
