#!/usr/bin/env python3
import pathlib

from PySide6 import QtCore

from .button import Button
from ...core.application_style import style_value
from ...enum.frame_control import FrameControl
from ...enum.frame_shape import FrameShape
from ...enum.event import Event
from ...tools import color_converter


class FrameCloseButton(Button):
    """Frame close button Element."""
    def __init__(
            self, frame_action: FrameControl = FrameControl.CLOSE,
            *args, **kwargs) -> None:
        super().__init__()
        # Args
        self.__frame_action = frame_action

        # Set
        self.size = 22
        
        self.class_id('FrameCloseButton')
        self.style_class = 'FrameCloseButton'
        self.mouse_press_signal.connect(self.__on_click)

    def __on_click(self) -> None:
        if self.__frame_action == FrameControl.MAX:
            if self._frame.shape == FrameShape.MAX:
                self._frame.shape = FrameShape.FRAME
            else:
                self._frame.shape = FrameShape.MAX
        elif self.__frame_action == FrameControl.FULL:
            if self._frame.shape == FrameShape.FULL:
                self._frame.shape = FrameShape.FRAME
            else:
                self._frame.shape = FrameShape.FULL
        elif self.__frame_action == FrameControl.MIN:
            if self._frame.shape == FrameShape.MIN:
                self._frame.shape = FrameShape.FRAME
            else:
                self._frame.shape = FrameShape.MIN

        elif self.__frame_action == FrameControl.CLOSE:
            self._frame._obj.close()

    def __str__(self) -> str:
        return "<class 'FrameCloseButton'>"


class FrameMaxButton(Button):
    """Frame maximize button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.size = 22
        self.class_id('FrameMaxButton')

        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon = str(self.__path) + '/static/control_button/plasma/'
        self.__sym = ''

        self.mouse_press_signal.connect(self.__on_click)
        self.mouse_hover_signal.connect(self.__on_hover)
        self.frame_signal.connect(self.__on_frame)

    def __on_frame(self) -> None:
        dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self._frame.style['[FrameMaxButton]']['background_color']))
        self.__sym = '-symbolic' if dark else ''

        self._frame.active_signal.connect(self.__on_active)
        self._frame.shape_signal.connect(self.__on_shape)

    def __on_click(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            self._frame.shape = FrameShape.FRAME
        else:
            self._frame.shape = FrameShape.MAX

    def __on_shape(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            icon = self.__icon + 'window-restore' + self.__sym + '.svg'
            self.icon = icon
            self._frame.style['[FrameMaxButton]']['icon'] = icon

            icon = self.__icon + 'window-restore-clicked' + self.__sym + '.svg'
            self._frame.style['[FrameMaxButton:clicked]']['icon'] = icon
        else:
            icon = self.__icon + 'go-up' + self.__sym + '.svg'
            self.icon = icon
            self._frame.style['[FrameMaxButton]']['icon'] = icon

            icon = self.__icon + 'go-up-clicked' + self.__sym + '.svg'
            self._frame.style['[FrameMaxButton:clicked]']['icon'] = icon

    def __on_active(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            icon = self.__icon + 'window-restore' + self.__sym + '.svg'
            self.icon = icon
            self._frame.style['[FrameMaxButton]']['icon'] = icon
        else:
            icon = self.__icon + 'go-up' + self.__sym + '.svg'
            self.icon = icon
            self._frame.style['[FrameMaxButton:hover]']['icon'] = icon

    def __on_hover(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            if self._frame.is_active() and self.is_mouse_hover():
                icon = (
                    self.__icon + 'window-restore-hover' + self.__sym + '.svg')
                self.icon = icon
                self._frame.style['[FrameMaxButton:hover]']['icon'] = icon
            else:
                icon = self.__icon + 'window-restore' + self.__sym + '.svg'
                self.icon = icon
                self._frame.style['[FrameMaxButton:hover]']['icon'] = icon
        else:
            if self._frame.is_active() and self.is_mouse_hover():
                icon = self.__icon + 'go-up-hover' + self.__sym + '.svg'
                self.icon = icon
                self._frame.style['[FrameMaxButton:hover]']['icon'] = icon
            else:
                icon = self.__icon + 'go-up' + self.__sym + '.svg'
                self.icon = icon
                self._frame.style['[FrameMaxButton:hover]']['icon'] = icon

    def __str__(self) -> str:
        return "<class 'FrameMaxButton'>"


class FrameMinButton(Button):
    """Frame minimize button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.size = 22
        self.class_id('FrameMinButton')
        self.mouse_press_signal.connect(self.__on_click)

    def __on_click(self) -> None:
        if self._frame.shape == FrameShape.MIN:
            self._frame.shape = FrameShape.FRAME
        else:
            self._frame.shape = FrameShape.MIN

    def __str__(self) -> str:
        return "<class 'FrameMinButton'>"
