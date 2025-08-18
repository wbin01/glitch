#!/usr/bin/env python3
import os
import pathlib
import pprint

from PySide6 import QtGui

from ..tools import color_converter, DesktopFile


class Style(object):
    """Application style.
    
    Manages style information according to the platform.
    """

    def __init__(self):
        """
        [Colors:Window]
        BackgroundAlternate=59,59,59
        BackgroundNormal=50,50,50    
        """
        self.__desktop = 'plasma'
        self.__conf = self.__get_sys_conf()

        self.__frame_bg = self.__sanitized_color(  # Alt 282828
            self.__conf['[Colors:Window]']['BackgroundNormal'], '#2A2A2A')
        self.__frame_bg_is_dark = color_converter.is_dark(
            color_converter.hex_to_rgba(self.__frame_bg))
        
        self.__frame_bd = self.__frame_bg
        if self.__frame_bg_is_dark:
            self.__frame_bd = color_converter.lighten_hex(self.__frame_bg, 15)

        # self.__frame_inactive_bg = self.__sanitized_color(
        #     self.__conf['[Colors:Header][Inactive]']['BackgroundNormal'],
        #     '#222')
        self.__frame_inactive_bg = color_converter.darken_hex(
            self.__frame_bg, 10)

        self.__frame_inactive_bd = self.__frame_inactive_bg
        if self.__frame_bg_is_dark:
            self.__frame_inactive_bd = color_converter.lighten_hex(
                self.__frame_inactive_bg, 15)

        self.style = {
            '[Button]': {
                'background_color': '#333',
                'border_color': '#444',
                'font_color': '#EEE',
                'icon_opacity': '1.0',
                },
            '[Button:inactive]': {
                'background_color': '#222',
                'border_color': '#333',
                'font_color': '#666',
                'icon_opacity': '0.3',
                },
            '[Button:hover]': {
                'background_color': '#383838',
                'border_color': '[Platform] accent_color #88',
                'font_color': '#EEE',
                'icon_opacity': '1.0',
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
                'border_color': '[Platform] accent_color',
                'border_radius': '10',
                },
            '[Frame:inactive]': {
                'background_color': '#222',
                'border_color': '[Platform] accent_color #55',
                'border_radius': '10',
                },
            '[Label]': {
                'font_color': '#EEE',
                },
            '[Label:inactive]': {
                'font_color': '#666',
                },
            '[MainFrame]': {
                'background_color': self.__frame_bg,
                'border_color': self.__frame_bd,
                'border_radius': '20, 20, 0, 0',
                },
            '[MainFrame:inactive]': {
                'background_color': self.__frame_inactive_bg,
                'border_color': self.__frame_inactive_bd,
                'border_radius': '10',
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
                'background_color': '#00000000',
                'border_color': '#00000000',
                'icon_opacity': '1.0',
                },
            '[ToolButton:inactive]': {
                'background_color': '#00000000',
                'border_color': '#00000000',
                'icon_opacity': '0.3',
                },
            '[ToolButton:hover]': {
                'background_color': '#00000000',
                'border_color': '[Platform] accent_color #88',
                'icon_opacity': '1.0',
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

    def __get_sys_conf(self) -> dict:
        conf_name = 'kdeglobals'
        conf_file = pathlib.Path(os.environ['HOME']) / '.config' / conf_name

        ini = {}
        if conf_file.exists():
            ini = DesktopFile(conf_file).content
        return ini

    def __sanitized_color(self, color, alt_color) -> str:
        color = color.split(',')
        len_color = len(color)

        if self.__desktop == 'plasma':
            if len_color == 3:
                color = int(color[0]), int(color[1]), int(color[2]), 255
            else:
                color = int(color[0]), int(color[1]), int(color[2]), int(color[3])
            return color_converter.rgba_to_hex(color)
        return alt_color

    def __q_sys_color(self) -> None:
        self.__palette = QtGui.QPalette()

        frame = self.__palette.color(QtGui.QPalette.Active, QtGui.QPalette.Window)
        self.__frame_color = color_converter.rgba_to_hex(frame.toTuple())
        print(self.__frame_color)

        text = self.__palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.WindowText)
        self.__label_color = color_converter.rgba_to_hex(text.toTuple())
        print(self.__label_color)

        accent = self.__palette.color(
            QtGui.QPalette.Active, QtGui.QPalette.Highlight)
        self.__accent_color = color_converter.rgba_to_hex(accent.toTuple())
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
    
    def __str__(self) -> str:
        return "<class 'Style'>"
