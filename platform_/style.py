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
        self.__accent_color = None

        self.__path = pathlib.Path(__file__).parent.parent
        self.__icon_path = str(self.__path) + '/static/control_button/plasma/'
        self.__plasma_close_button_with_circle = False
        self.__symbolic = ''
        self.__main_frame_bg = None

    def accent_color(self) -> str:
        """..."""
        if not self.__conf:
            self.__conf = self.__get_sys_conf()

        if not self.__accent_color:
            self.__accent_color = self.__color_to_hex(
                self.__conf['[General]']['AccentColor'], '#FF3C8CBD')

        return self.__accent_color

    def print(self) -> None:
        for key, value in self.style().items():
            print(key)
            for k, v in value.items():
                print(f'{k}: {v}')
            print()

    def style(self) -> dict:
        """..."""
        if self.__style:
            return self.__style

        if not self.__conf:
            self.__conf = self.__get_sys_conf()

        if not self.__main_frame_bg:
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
                'icon_opacity': self.__button_hv_io,
                },
            '[Button:clicked]': {
                'background_color': self.__button_ck_bg,
                'border_color': self.__button_ck_bd,
                'font_color': self.__button_ck_fg,
                'icon_opacity': self.__button_ck_io,
                },
            '[Button:checked]': {
                'background_color': self.__button_ch_bg,
                'border_color': self.__button_ch_bd,
                'font_color': self.__button_ch_fg,
                'icon_opacity': self.__button_ch_io,
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
                'icon_opacity': self.__button_ch_hv_io,
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
            '[FrameCloseButton]': {
                'background_color': self.__frame_close_button_bg,
                'border_color': self.__frame_close_button_bd,
                'font_color': self.__frame_close_button_fg,
                'icon_opacity': self.__frame_close_button_io,
                'icon': self.__frame_close_button_i,
                'border_width': '0',
                'border_radius': self.__frame_close_button_rd,
                },
            '[FrameCloseButton:inactive]': {
                'background_color': self.__frame_close_button_in_bg,
                'border_color': self.__frame_close_button_in_bd,
                'font_color': self.__frame_close_button_in_fg,
                'icon_opacity': self.__frame_close_button_in_io,
                'icon': self.__frame_close_button_in_i,
                },
            '[FrameCloseButton:hover]': {
                'background_color': self.__frame_close_button_hv_bg,
                'border_color': self.__frame_close_button_hv_bd,
                'font_color': self.__frame_close_button_hv_fg,
                'icon_opacity': self.__frame_close_button_hv_io,
                'icon': self.__frame_close_button_hv_i,
                },
            '[FrameCloseButton:clicked]': {
                'background_color': self.__frame_close_button_ck_bg,
                'border_color': self.__frame_close_button_ck_bd,
                'font_color': self.__frame_close_button_ck_fg,
                'icon_opacity': self.__frame_close_button_ck_io,
                'icon': self.__frame_close_button_ck_i,
                },
            '[FrameFullButton]': {
                'background_color': self.__frame_full_button_bg,
                'border_color': self.__frame_full_button_bd,
                'font_color': self.__frame_full_button_fg,
                'icon_opacity': self.__frame_full_button_io,
                'icon': self.__frame_full_button_i,
                'restore_icon': self.__frame_full_button_ir,
                'border_width': '0',
                'border_radius': self.__frame_full_button_rd,
                },
            '[FrameFullButton:inactive]': {
                'background_color': self.__frame_full_button_in_bg,
                'border_color': self.__frame_full_button_in_bd,
                'font_color': self.__frame_full_button_in_fg,
                'icon_opacity': self.__frame_full_button_in_io,
                'icon': self.__frame_full_button_in_i,
                'restore_icon': self.__frame_full_button_in_ir,
                },
            '[FrameFullButton:hover]': {
                'background_color': self.__frame_full_button_hv_bg,
                'border_color': self.__frame_full_button_hv_bd,
                'font_color': self.__frame_full_button_hv_fg,
                'icon_opacity': self.__frame_full_button_hv_io,
                'icon': self.__frame_full_button_hv_i,
                'restore_icon': self.__frame_full_button_hv_ir,
                },
            '[FrameFullButton:clicked]': {
                'background_color': self.__frame_full_button_ck_bg,
                'border_color': self.__frame_full_button_ck_bd,
                'font_color': self.__frame_full_button_ck_fg,
                'icon_opacity': self.__frame_full_button_ck_io,
                'icon': self.__frame_full_button_ck_i,
                'restore_icon': self.__frame_full_button_ck_ir,
                },
            '[FrameMaxButton]': {
                'background_color': self.__frame_max_button_bg,
                'border_color': self.__frame_max_button_bd,
                'font_color': self.__frame_max_button_fg,
                'icon_opacity': self.__frame_max_button_io,
                'icon': self.__frame_max_button_i,
                'restore_icon': self.__frame_max_button_ir,
                'border_width': '0',
                'border_radius': self.__frame_max_button_rd,
                },
            '[FrameMaxButton:inactive]': {
                'background_color': self.__frame_max_button_in_bg,
                'border_color': self.__frame_max_button_in_bd,
                'font_color': self.__frame_max_button_in_fg,
                'icon_opacity': self.__frame_max_button_in_io,
                'icon': self.__frame_max_button_in_i,
                'restore_icon': self.__frame_max_button_in_ir,
                },
            '[FrameMaxButton:hover]': {
                'background_color': self.__frame_max_button_hv_bg,
                'border_color': self.__frame_max_button_hv_bd,
                'font_color': self.__frame_max_button_hv_fg,
                'icon_opacity': self.__frame_max_button_hv_io,
                'icon': self.__frame_max_button_hv_i,
                'restore_icon': self.__frame_max_button_hv_ir,
                },
            '[FrameMaxButton:clicked]': {
                'background_color': self.__frame_max_button_ck_bg,
                'border_color': self.__frame_max_button_ck_bd,
                'font_color': self.__frame_max_button_ck_fg,
                'icon_opacity': self.__frame_max_button_ck_io,
                'icon': self.__frame_max_button_ck_i,
                'restore_icon': self.__frame_max_button_ck_ir,
                },
            '[FrameMinButton]': {
                'background_color': self.__frame_min_button_bg,
                'border_color': self.__frame_min_button_bd,
                'font_color': self.__frame_min_button_fg,
                'icon_opacity': self.__frame_min_button_io,
                'icon': self.__frame_min_button_i,
                'border_width': '0',
                'border_radius': self.__frame_min_button_rd,
                },
            '[FrameMinButton:inactive]': {
                'background_color': self.__frame_min_button_in_bg,
                'border_color': self.__frame_min_button_in_bd,
                'font_color': self.__frame_min_button_in_fg,
                'icon_opacity': self.__frame_min_button_in_io,
                'icon': self.__frame_min_button_in_i,
                },
            '[FrameMinButton:hover]': {
                'background_color': self.__frame_min_button_hv_bg,
                'border_color': self.__frame_min_button_hv_bd,
                'font_color': self.__frame_min_button_hv_fg,
                'icon_opacity': self.__frame_min_button_hv_io,
                'icon': self.__frame_min_button_hv_i,
                },
            '[FrameMinButton:clicked]': {
                'background_color': self.__frame_min_button_ck_bg,
                'border_color': self.__frame_min_button_ck_bd,
                'font_color': self.__frame_min_button_ck_fg,
                'icon_opacity': self.__frame_min_button_ck_io,
                'icon': self.__frame_min_button_ck_i,
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

        # It needs to have this order
        self.__style_main_frame()
        self.__style_frame()
        self.__style_label()
        self.__style_button()
        self.__style_tool_button()
        self.__style_frame_close_button()
        self.__style_frame_full_button()
        self.__style_frame_max_button()
        self.__style_frame_min_button()
        self.__style_panel()

    def __style_main_frame(self) -> None:
        self.__main_frame_fg = self.__color_to_hex(
            self.__conf['[Colors:Window]']['ForegroundNormal'], '#FFFFFF')
        
        self.__main_frame_bg = self.__color_to_hex(  # Alt 282828
            self.__conf['[Colors:Window]']['BackgroundNormal'], '#2A2A2A')

        self.__main_frame_is_dark = colr.is_dark(
            colr.hex_to_rgba(self.__main_frame_bg))

        self.__main_frame_bd = self.__main_frame_bg
        if self.__main_frame_is_dark:
            self.__main_frame_bd = colr.lighten_hex(self.__main_frame_bg, 15)
        
        self.__main_frame_rd = '8, 8, 8, 8'
        self.__main_frame_io = '1.0'

        # Inactive
        if self.__inactive_as_platform:
            # [Colors:Header][Inactive]][BackgroundNormal]
            self.__main_frame_in_fg = self.__main_frame_fg
            self.__main_frame_in_bg = self.__main_frame_bg
            self.__main_frame_in_io = self.__main_frame_io
            self.__main_frame_in_bd = self.__main_frame_bd
        else:
            self.__main_frame_in_fg = '#99' + self.__main_frame_fg[3:]
            self.__main_frame_in_bg = colr.darken_hex(self.__main_frame_bg, 4)
            self.__main_frame_in_io = '0.5'

            self.__main_frame_in_bd = self.__main_frame_in_bg
            if self.__main_frame_is_dark:
                self.__main_frame_in_bd = colr.lighten_hex(
                    self.__main_frame_in_bg, 5)

    def __style_frame(self) -> None:
        self.__frame_is_dark = self.__main_frame_is_dark
        self.__frame_fg = self.__main_frame_fg
        self.__frame_bg = self.__main_frame_bg
        self.__frame_bd = self.__main_frame_bd
        self.__frame_rd = self.__main_frame_rd[0]
        self.__frame_in_fg = self.__main_frame_in_fg
        self.__frame_in_bg = self.__main_frame_in_bg
        self.__frame_in_bd = self.__main_frame_in_bd

    def __style_label(self) -> None:
        self.__label_fg = self.__main_frame_fg
        self.__label_bg = self.__main_frame_bg
        self.__label_in_fg = self.__main_frame_in_fg
        self.__label_in_bg = self.__main_frame_in_bg

    def __style_button(self) -> None:
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
        self.__button_hv_bd = '#99' + self.__color_to_hex(
            self.__conf['[Colors:Button]']['DecorationHover'], '#3C8CBD')[3:]
        self.__button_hv_io = self.__button_io

        self.__button_ck_fg = self.__button_fg
        self.__button_ck_bg = '#33' + self.__button_hv_bd[3:]
        self.__button_ck_bd = self.__button_hv_bd
        self.__button_ck_io = self.__button_io

        self.__button_ch_fg = self.__button_fg
        self.__button_ch_bg = '#AA' + self.__button_bd[3:]
        self.__button_ch_bd = self.__button_bd
        self.__button_ch_io = self.__button_io

        self.__button_ch_in_fg = self.__button_in_fg

        if self.__inactive_as_platform:
            self.__button_ch_in_bg = self.__button_ch_bg
        else:
            self.__button_ch_in_bg = '#33' + self.__button_ch_bg[3:]

        self.__button_ch_in_bd = self.__button_in_bd
        self.__button_ch_in_io = self.__button_in_io
        
        self.__button_ch_hv_fg = self.__button_ch_fg
        self.__button_ch_hv_bg = self.__button_ch_bg
        self.__button_ch_hv_bd = self.__button_hv_bd
        self.__button_ch_hv_io = self.__button_ch_io

    def __style_tool_button(self) -> None:
        self.__tool_button_bg = self.__main_frame_bg
        self.__tool_button_bd = self.__main_frame_bg
        self.__tool_button_io = self.__button_io
        self.__tool_button_rd = self.__button_rd

        self.__tool_button_in_bg = self.__main_frame_in_bg
        self.__tool_button_in_bd = self.__main_frame_in_bg
        self.__tool_button_in_io = self.__button_in_io
        
        self.__tool_button_hv_bg = self.__tool_button_bg
        self.__tool_button_hv_bd = self.__button_hv_bd
        self.__tool_button_hv_io = self.__tool_button_io

        self.__tool_button_ck_bg = self.__button_ck_bg
        self.__tool_button_ck_bd = self.__button_ck_bd
        self.__tool_button_ck_io = self.__button_ck_io

        self.__tool_button_ch_bg = '#88' + self.__button_ch_bg[3:]
        self.__tool_button_ch_bd = self.__button_ch_bd
        self.__tool_button_ch_io = self.__button_ch_io

        if self.__inactive_as_platform:
            self.__tool_button_ch_in_bg = self.__tool_button_ch_bg
            self.__tool_button_ch_in_bd = self.__tool_button_ch_bd
        else:
            self.__tool_button_ch_in_bg = '#33' + self.__tool_button_ch_bg[3:]
            self.__tool_button_ch_in_bd = '#33' + self.__tool_button_ch_bd[3:]

        self.__tool_button_ch_in_io = self.__tool_button_in_io

        self.__tool_button_ch_hv_bg = self.__tool_button_ch_bg
        self.__tool_button_ch_hv_bd = self.__tool_button_hv_bd
        self.__tool_button_ch_hv_io = self.__tool_button_ch_io

    def __style_frame_close_button(self) -> None:
        icon = 'window-close'
        ico = icon if self.__plasma_close_button_with_circle else icon + '-b'
        self.__symbolic = '-symbolic' if self.__main_frame_is_dark else ''

        self.__frame_close_button_bg = self.__main_frame_bg
        self.__frame_close_button_bd = self.__main_frame_bg
        self.__frame_close_button_fg = self.__main_frame_fg
        self.__frame_close_button_io = self.__button_io
        self.__frame_close_button_i = (
            self.__icon_path + ico + self.__symbolic + '.svg')
        self.__frame_close_button_rd = self.__tool_button_rd
        self.__frame_close_button_in_bg = self.__main_frame_in_bg
        self.__frame_close_button_in_bd = self.__main_frame_in_bg
        self.__frame_close_button_in_fg = self.__main_frame_in_fg
        self.__frame_close_button_in_io = self.__button_in_io
        self.__frame_close_button_in_i = (
            self.__icon_path + ico + '-inactive' + self.__symbolic + '.svg')
        self.__frame_close_button_hv_bg = self.__main_frame_bg
        self.__frame_close_button_hv_bd = self.__main_frame_bg
        self.__frame_close_button_hv_fg = self.__main_frame_fg
        self.__frame_close_button_hv_io = self.__button_hv_io
        self.__frame_close_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__frame_close_button_ck_bg = self.__main_frame_bg
        self.__frame_close_button_ck_bd = self.__main_frame_bg
        self.__frame_close_button_ck_fg = self.__main_frame_fg
        self.__frame_close_button_ck_io = self.__button_ck_io
        self.__frame_close_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __style_frame_full_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__frame_full_button_bg = self.__frame_close_button_bg
        self.__frame_full_button_bd = self.__frame_close_button_bd
        self.__frame_full_button_fg = self.__frame_close_button_fg
        self.__frame_full_button_io = self.__frame_close_button_io
        self.__frame_full_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__frame_full_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__frame_full_button_rd = self.__tool_button_rd
        self.__frame_full_button_in_bg = self.__frame_close_button_in_bg
        self.__frame_full_button_in_bd = self.__frame_close_button_in_bd
        self.__frame_full_button_in_fg = self.__frame_close_button_in_fg
        self.__frame_full_button_in_io = self.__frame_close_button_in_io
        self.__frame_full_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__frame_full_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic + '.svg')
        self.__frame_full_button_hv_bg = self.__frame_close_button_hv_bg
        self.__frame_full_button_hv_bd = self.__frame_close_button_hv_bd
        self.__frame_full_button_hv_fg = self.__frame_close_button_hv_fg
        self.__frame_full_button_hv_io = self.__frame_close_button_hv_io
        self.__frame_full_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__frame_full_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')
        self.__frame_full_button_ck_bg = self.__frame_close_button_ck_bg
        self.__frame_full_button_ck_bd = self.__frame_close_button_ck_bd
        self.__frame_full_button_ck_fg = self.__frame_close_button_ck_fg
        self.__frame_full_button_ck_io = self.__frame_close_button_ck_io
        self.__frame_full_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__frame_full_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __style_frame_max_button(self) -> None:
        icon = 'go-up'
        restore = 'window-restore'
        self.__frame_max_button_bg = self.__frame_close_button_bg
        self.__frame_max_button_bd = self.__frame_close_button_bd
        self.__frame_max_button_fg = self.__frame_close_button_fg
        self.__frame_max_button_io = self.__frame_close_button_io
        self.__frame_max_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__frame_max_button_ir = (
            self.__icon_path + restore + self.__symbolic + '.svg')
        self.__frame_max_button_rd = self.__tool_button_rd
        self.__frame_max_button_in_bg = self.__frame_close_button_in_bg
        self.__frame_max_button_in_bd = self.__frame_close_button_in_bd
        self.__frame_max_button_in_fg = self.__frame_close_button_in_fg
        self.__frame_max_button_in_io = self.__frame_close_button_in_io
        self.__frame_max_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__frame_max_button_in_ir = (
            self.__icon_path + restore + '-inactive' + self.__symbolic + '.svg')
        self.__frame_max_button_hv_bg = self.__frame_close_button_hv_bg
        self.__frame_max_button_hv_bd = self.__frame_close_button_hv_bd
        self.__frame_max_button_hv_fg = self.__frame_close_button_hv_fg
        self.__frame_max_button_hv_io = self.__frame_close_button_hv_io
        self.__frame_max_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__frame_max_button_hv_ir = (
            self.__icon_path + restore + '-hover' + self.__symbolic + '.svg')
        self.__frame_max_button_ck_bg = self.__frame_close_button_ck_bg
        self.__frame_max_button_ck_bd = self.__frame_close_button_ck_bd
        self.__frame_max_button_ck_fg = self.__frame_close_button_ck_fg
        self.__frame_max_button_ck_io = self.__frame_close_button_ck_io
        self.__frame_max_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')
        self.__frame_max_button_ck_ir = (
            self.__icon_path + restore + '-clicked' + '.svg')

    def __style_frame_min_button(self) -> None:
        icon = 'go-down'
        self.__frame_min_button_bg = self.__frame_close_button_bg
        self.__frame_min_button_bd = self.__frame_close_button_bd
        self.__frame_min_button_fg = self.__frame_close_button_fg
        self.__frame_min_button_io = self.__frame_close_button_io
        self.__frame_min_button_i = (
            self.__icon_path + icon + self.__symbolic + '.svg')
        self.__frame_min_button_rd = self.__tool_button_rd
        self.__frame_min_button_in_bg = self.__frame_close_button_in_bg
        self.__frame_min_button_in_bd = self.__frame_close_button_in_bd
        self.__frame_min_button_in_fg = self.__frame_close_button_in_fg
        self.__frame_min_button_in_io = self.__frame_close_button_in_io
        self.__frame_min_button_in_i = (
            self.__icon_path + icon + '-inactive' + self.__symbolic + '.svg')
        self.__frame_min_button_hv_bg = self.__frame_close_button_hv_bg
        self.__frame_min_button_hv_bd = self.__frame_close_button_hv_bd
        self.__frame_min_button_hv_fg = self.__frame_close_button_hv_fg
        self.__frame_min_button_hv_io = self.__frame_close_button_hv_io
        self.__frame_min_button_hv_i = (
            self.__icon_path + icon + '-hover' + self.__symbolic + '.svg')
        self.__frame_min_button_ck_bg = self.__frame_close_button_ck_bg
        self.__frame_min_button_ck_bd = self.__frame_close_button_ck_bd
        self.__frame_min_button_ck_fg = self.__frame_close_button_ck_fg
        self.__frame_min_button_ck_io = self.__frame_close_button_ck_io
        self.__frame_min_button_ck_i = (
            self.__icon_path + icon + '-clicked' + '.svg')

    def __style_panel(self) -> None:
        self.__panel_bg = '#FA' + colr.darken_hex(self.__main_frame_bg, 5)[3:]
        self.__panel_bd = self.__panel_bg
        self.__panel_rd = self.__main_frame_rd
        self.__panel_in_bg = colr.darken_hex(self.__main_frame_in_bg, 5)
        self.__panel_in_bd = self.__panel_in_bg
