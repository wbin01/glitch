#!/usr/bin/env python3
import os
import pathlib
import pprint

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

        self.__button_fg = None
        self.__button_bg = None
        self.__button_bd = None
        self.__button_rd = None
        self.__button_io = None
        self.__button_in_fg = None
        self.__button_in_bg = None
        self.__button_in_bd = None
        self.__button_in_io = None
        self.__button_hv_fg = None
        self.__button_hv_bg = None
        self.__button_hv_bd = None
        self.__button_hv_io = None
        self.__button_ck_fg = None
        self.__button_ck_bg = None
        self.__button_ck_bd = None
        self.__button_ch_fg = None
        self.__button_ch_bg = None
        self.__button_ch_bd = None
        self.__button_ch_in_fg = None
        self.__button_ch_in_bg = None
        self.__button_ch_in_bd = None
        self.__button_ch_hv_fg = None
        self.__button_ch_hv_bg = None
        self.__button_ch_hv_bd = None

        self.__button_ck_in_fg = None
        self.__button_ck_in_bg = None
        self.__button_ck_in_bd = None

        self.__frame_is_dark = None
        self.__frame_fg = None
        self.__frame_bg = None
        self.__frame_bd = None
        self.__frame_rd = None
        self.__frame_in_fg = None
        self.__frame_in_bg = None
        self.__frame_in_bd = None

        self.__label_fg = None
        self.__label_bg = None
        self.__label_in_fg = None
        self.__label_in_bg = None

        self.__main_frame_is_dark = None
        self.__main_frame_fg = None
        self.__main_frame_bg = None
        self.__main_frame_bd = None
        self.__main_frame_rd = None
        self.__main_frame_io = None
        self.__main_frame_in_fg = None
        self.__main_frame_in_bg = None
        self.__main_frame_in_bd = None
        self.__main_frame_in_io = None

        self.__tool_button_bg = None
        self.__tool_button_bd = None
        self.__tool_button_rd = None
        self.__tool_button_io = None
        self.__tool_button_in_bg = None
        self.__tool_button_in_bd = None
        self.__tool_button_in_io = None
        self.__tool_button_hv_bg = None
        self.__tool_button_hv_bd = None
        self.__tool_button_hv_io = None
        self.__tool_button_ck_bg = None
        self.__tool_button_ck_bd = None
        self.__tool_button_ch_bg = None
        self.__tool_button_ch_bd = None
        self.__tool_button_ch_in_bg = None
        self.__tool_button_ch_in_bd = None
        self.__tool_button_ch_hv_bg = None
        self.__tool_button_ch_hv_bd = None


    def style(self) -> dict:
        if self.__style:
            return self.__style

        if not self.__conf:
            self.__conf = self.__get_sys_conf()

        if not self.__main_frame_bg:
            self.__set_styles_from_platform()

        self.__style = {
            '[Button]': {
                'background_color': self.__button_bg,
                'border_color': self.__button_bd,
                'font_color': self.__button_fg,
                'icon_opacity': self.__button_io,
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
                'icon_opacity': self.__button_hv_io,
                },
            '[Button:clicked]': {
                'background_color': '[Platform] accent_color #33',
                'border_color': '[Platform] accent_color #88',
                'font_color': '#FFF',
                'icon_opacity': '1.0',
                },
            '[Button:checked]': {
                'background_color': '#484848',
                'border_color': '#555',
                'font_color': '#EEE',
                'icon_opacity': '1.0',
                },
            '[Button:checked:inactive]': {
                'background_color': '#2A2A2A',
                'border_color': '#333',
                'font_color': '#666',
                'icon_opacity': '0.3',
                },
            '[Button:checked:hover]': {
                'background_color': '#484848',
                'border_color': '[Platform] accent_color #88',
                'font_color': '#EEE',
                'icon_opacity': '1.0',
                },
            '[Frame]': {
                'background_color': self.__frame_bg,
                'border_color': self.__frame_bd,
                'border_radius': self.__frame_rd,
                },
            '[Frame:inactive]': {
                'background_color': self.__frame_in_bg,
                'border_color': self.__frame_in_bd,
                # 'border_radius': '10',
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
                'background_color': self.__main_frame_bg,
                'border_color': self.__main_frame_bd,
                'border_radius': self.__main_frame_rd,
                },
            '[MainFrame:inactive]': {
                'background_color': self.__main_frame_in_bg,
                'border_color': self.__main_frame_in_bd,
                # 'border_radius': '10',
                },
            '[Panel]': {
                'background_color': '#EF222222',
                'border_color': '#222222',
                'border_radius': '10',
                },
            '[Panel:inactive]': {
                'background_color': '#202020',
                'border_color': '#202020',
                'border_radius': '10',
                },
            '[Platform]': {
                'accent_color': '#3C8CBD',
                },
            '[ToolButton]': {
                'background_color': self.__tool_button_bg,
                'border_color': self.__tool_button_bd,
                'icon_opacity': self.__tool_button_io,
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
                'background_color': '[Platform] accent_color #33',
                'border_color': '[Platform] accent_color #88',
                'icon_opacity': '1.0',
                },
            '[ToolButton:checked]': {
                'background_color': '#333',
                'border_color': '#444',
                'icon_opacity': '1.0',
                },
            '[ToolButton:checked:inactive]': {
                'background_color': '#222',
                'border_color': '#333',
                'icon_opacity': '0.3',
                },
            '[ToolButton:checked:hover]': {
                'background_color': '#333',
                'border_color': '[Platform] accent_color #88',
                'icon_opacity': '1.0',
                },
            }
        return self.__style

    def __get_sys_conf(self) -> dict:
        conf_name = 'kdeglobals'
        conf_file = pathlib.Path(os.environ['HOME']) / '.config' / conf_name

        ini = {}
        if conf_file.exists():
            ini = DesktopFile(conf_file).content
        return ini

    def __color_to_hex(self, color, alt_color) -> str:
        color = color.split(',')
        len_color = len(color)

        if self.__desktop == 'plasma':
            if len_color == 3:
                color = int(color[0]), int(color[1]), int(color[2]), 255
            else:
                color = int(color[0]), int(color[1]), int(color[2]), int(color[3])
            return colr.rgba_to_hex(color)
        return alt_color

    def __set_styles_from_platform(self) -> None:
        # MainFrame
        self.__main_frame_fg = self.__color_to_hex(
            self.__conf['[Colors:Window]']['ForegroundNormal'], '#FFFFFF')

        self.__main_frame_bg = self.__color_to_hex(  # Alt 282828
            self.__conf['[Colors:Window]']['BackgroundNormal'], '#2A2A2A')

        self.__main_frame_is_dark = colr.is_dark(
            colr.hex_to_rgba(self.__main_frame_bg))
        
        self.__main_frame_bd = self.__main_frame_bg
        if self.__main_frame_is_dark:
            self.__main_frame_bd = colr.lighten_hex(self.__main_frame_bg, 15)

        self.__main_frame_rd = 6, 6, 0, 0
        self.__main_frame_io = '1.0'
        self.__inactive_as_platform = True
        if self.__inactive_as_platform:
            # [Colors:Header][Inactive]][BackgroundNormal]
            self.__main_frame_in_fg = self.__main_frame_fg
            self.__main_frame_in_bg = self.__main_frame_bg
            self.__main_frame_in_io = self.__main_frame_io
            self.__main_frame_in_bd = self.__main_frame_bd
        else:
            self.__main_frame_in_fg = '#88' + self.__main_frame_fg[3:]
            self.__main_frame_in_bg = colr.darken_hex(self.__main_frame_bg, 10)
            self.__main_frame_in_io = '0.5'

            self.__main_frame_in_bd = self.__main_frame_in_bg
            if self.__main_frame_is_dark:
                self.__main_frame_in_bd = colr.lighten_hex(
                    self.__main_frame_in_bg, 5)
        # Frame
        self.__frame_is_dark = self.__main_frame_is_dark
        self.__frame_fg = self.__main_frame_fg
        self.__frame_bg = self.__main_frame_bg
        self.__frame_bd = self.__main_frame_bd
        self.__frame_rd = self.__main_frame_rd[0]
        self.__frame_in_fg = self.__main_frame_in_fg
        self.__frame_in_bg = self.__main_frame_in_bg
        self.__frame_in_bd = self.__main_frame_in_bd

        # Label
        self.__label_fg = self.__main_frame_fg
        self.__label_bg = self.__main_frame_bg
        self.__label_in_fg = self.__main_frame_in_fg
        self.__label_in_bg = self.__main_frame_in_bg

        # Button
        self.__button_fg = self.__main_frame_fg

        self.__button_bg = self.__color_to_hex(
            self.__conf['[Colors:Button]']['BackgroundNormal'], '#33333333')

        if self.__main_frame_is_dark:
            self.__button_bd = colr.lighten_hex(self.__button_bg, 35)
        else:
            self.__button_bd = colr.darken_hex(self.__button_bg, 35)

        self.__button_rd = '6'

        self.__button_io = self.__main_frame_io

        self.__button_in_fg = self.__main_frame_in_fg

        if self.__inactive_as_platform:
            self.__button_in_bg = self.__button_bg
            self.__button_in_bd = self.__button_bd
        else:
            self.__button_in_bg = self.__main_frame_in_bg
            self.__button_in_bd = '#33' + self.__button_bd[3:]
        
        self.__button_in_io = self.__main_frame_in_io

        self.__button_hv_fg = self.__button_fg
        self.__button_hv_bg = self.__button_bg
        self.__button_hv_bd = self.__color_to_hex(
            self.__conf['[Colors:Button]']['DecorationHover'], '#3C8CBD')
        self.__button_hv_io = self.__button_io

        self.__button_ck_fg = None
        self.__button_ck_bg = None
        self.__button_ck_bd = None

        self.__button_ch_fg = None
        self.__button_ch_bg = None
        self.__button_ch_bd = None

        self.__button_ch_in_fg = None
        self.__button_ch_in_bg = None
        self.__button_ch_in_bd = None
        
        self.__button_ch_hv_fg = None
        self.__button_ch_hv_bg = None
        self.__button_ch_hv_bd = None


        # ToolButton
        self.__tool_button_bg = self.__main_frame_bg
        self.__tool_button_bd = self.__main_frame_bg
        # self.__tool_button_rd = None
        self.__tool_button_io = self.__button_io

        self.__tool_button_in_bg = self.__main_frame_in_bg
        self.__tool_button_in_bd = self.__main_frame_in_bg
        self.__tool_button_in_io = self.__button_in_io
        
        self.__tool_button_hv_bg = self.__tool_button_bg
        self.__tool_button_hv_bd = self.__button_hv_bd
        self.__tool_button_hv_io = self.__tool_button_io

        self.__tool_button_ck_bg = None
        self.__tool_button_ck_bd = None

        self.__tool_button_ch_bg = None
        self.__tool_button_ch_bd = None

        self.__tool_button_ch_in_bg = None
        self.__tool_button_ch_in_bd = None

        self.__tool_button_ch_hv_bg = None
        self.__tool_button_ch_hv_bd = None

    def __q_sys_color(self) -> None:
        self.__palette = QtGui.QPalette()

        frame = self.__palette.color(QtGui.QPalette.Active, QtGui.QPalette.Window)
        self.__frame_color = colr.rgba_to_hex(frame.toTuple())
        print(self.__frame_color)

        text = self.__palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText)
        self.__label_color = colr.rgba_to_hex(text.toTuple())
        print(self.__label_color)

        accent = self.__palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        self.__accent_color = colr.rgba_to_hex(accent.toTuple())
        print(self.__accent_color)

        print('---')
        # Background color
        self.background_color = QtGui.QColor(
            QtGui.QPalette().color(
                QtGui.QPalette.Active, QtGui.QPalette.Midlight))
        print(self.background_color)

        # Background color
        self.palette_color = QtGui.QColor(
            QtGui.QPalette().color(  # ToolTipBase Button Window AlternateBase
                QtGui.QPalette.Active, QtGui.QPalette.Window))
        print(self.palette_color)

    def clear_cache(self) -> None:
        """Clear properties cache"""
        self.__style = None
        self.__conf = None

        self.__main_frame_bg = None
        self.__main_frame_bd = None
        self.__main_frame_is_dark = None
        self.__main_frame_in_bg = None
        self.__main_frame_in_bd = None
    
    def __str__(self) -> str:
        return "<class 'Style'>"
