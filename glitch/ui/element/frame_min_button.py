#!/usr/bin/env python3
import pathlib

from .button import Button
from ...enum.frame_shape import FrameShape
from ...tools import color_converter


class FrameMinButton(Button):
    """Frame close button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon = str(self.__path) + '/static/control_button/plasma/'
        self.__sym = ''
        self.__follow_plasma = True

        # Set
        self.size = 22
        
        self.class_id('FrameMinButton')
        self.style_class = 'FrameMinButton'
        self.mouse_press_signal.connect(self.__on_click)
        self.mouse_hover_signal.connect(self.__on_hover)

        self.frame_signal.connect(self.__on_frame)

    def __on_frame(self) -> None:
        dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self._frame.style['[FrameMinButton]']['background_color']))
        self.__sym = '-symbolic' if dark else ''

        self._frame.active_signal.connect(self.__on_active)

    def __on_active(self) -> None:
        icox = self.__icon + 'go-down-clicked' + self.__sym + '.svg'
        self._frame.style['[FrameMinButton:clicked]']['icon'] = icox

    def __on_click(self) -> None:
        self._frame.shape = FrameShape.MIN

    def __on_hover(self) -> None:
        if self.is_mouse_hover():
            if self._frame.is_active():
                icon = self.__icon + 'go-down-hover'
            else:
                if self.__follow_plasma:
                    icon = self.__icon + 'go-down-inactive-hover'
                else:
                    icon = self.__icon + 'go-down'
        else:
            icon = self.__icon + 'go-down'

        self.icon = icon  + self.__sym + '.svg'

    def __str__(self) -> str:
        return "<class 'FrameMinButton'>"
