#!/usr/bin/env python3
import pathlib

from .button import Button
from ...enum.frame_shape import FrameShape
from ...tools import color_converter


class FrameCloseButton(Button):
    """Frame close button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon = str(self.__path) + '/static/control_button/plasma/'
        self.__sym = ''
        self.__follow_plasma = True
        self.__follow_plasma_c = False

        # Set
        self.size = 22
        
        self.class_id('FrameCloseButton')
        self.style_class = 'FrameCloseButton'
        self.mouse_press_signal.connect(self.__on_click)
        self.mouse_hover_signal.connect(self.__on_hover)

        self.frame_signal.connect(self.__on_frame)

    def __on_frame(self) -> None:
        dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self._frame.style['[FrameCloseButton]']['background_color']))
        self.__sym = '-symbolic' if dark else ''

        self._frame.active_signal.connect(self.__on_active)

    def __on_active(self) -> None:
        icox = self.__icon + 'window-close-clicked' + self.__sym + '.svg'
        self._frame.style['[FrameCloseButton:clicked]']['icon'] = icox

    def __on_click(self) -> None:
        self._frame._obj.close()

    def __on_hover(self) -> None:
        if self.is_mouse_hover():
            if self._frame.is_active():
                icon = self.__icon + 'window-close-b-hover'
            else:
                if self.__follow_plasma:
                    icon = self.__icon + 'window-close-b-inactive-hover'
                else:
                    icon = self.__icon + 'window-close-b'
        else:
            icon = self.__icon + 'window-close-b'

        if self.__follow_plasma_c:
            icon = icon.replace('-b', '')
        self.icon = icon  + self.__sym + '.svg'

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
        self.__follow_plasma = True

        self.mouse_press_signal.connect(self.__on_click)
        self.mouse_hover_signal.connect(self.__on_hover)
        self.frame_signal.connect(self.__on_frame)

    def __on_frame(self) -> None:
        dark = color_converter.is_dark(color_converter.hex_to_rgba(
            self._frame.style['[FrameMaxButton]']['background_color']))
        self.__sym = '-symbolic' if dark else ''

        self._frame.active_signal.connect(self.__on_active)
        self._frame.shape_signal.connect(self.__on_active)

    def __on_active(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            icon = self.__icon + 'window-restore'
            ico = self.__icon + 'window-restore-clicked' + self.__sym + '.svg'
        else:
            icon = self.__icon + 'go-up'
            ico = self.__icon + 'go-up-clicked' + self.__sym + '.svg'
        self.icon = icon + self.__sym + '.svg'
        self._frame.style['[FrameMaxButton:clicked]']['icon'] = ico


    def __on_hover(self) -> None:
        if self.is_mouse_hover():
            if self.__follow_plasma:
                if self._frame.shape == FrameShape.MAX:
                    icon = self.__icon + 'window-restore-hover'
                else:
                    icon = self.__icon + 'go-up-hover'
                self.icon = icon  + self.__sym + '.svg'
        else:
            if self._frame.shape == FrameShape.MAX:
                icon = self.__icon + 'window-restore'
            else:
                icon = self.__icon + 'go-up'
            self.icon = icon + self.__sym + '.svg'

    def __on_click(self) -> None:
        if self._frame.shape == FrameShape.MAX:
            self._frame.shape = FrameShape.FRAME
        else:
            self._frame.shape = FrameShape.MAX

    def __str__(self) -> str:
        return "<class 'FrameMaxButton'>"


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
