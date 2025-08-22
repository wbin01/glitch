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
            if self._application_frame.shape == FrameShape.MAX:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.MAX
        elif self.__frame_action == FrameControl.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.FULL
        elif self.__frame_action == FrameControl.MIN:
            if self._application_frame.shape == FrameShape.MIN:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.MIN

        elif self.__frame_action == FrameControl.CLOSE:
            self._application_frame._obj.close()

    def __str__(self) -> str:
        return "<class 'FrameCloseButton'>"


class FrameMaxButton(Button):
    """Frame maximize button Element."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.size = 22
        self.class_id('FrameMaxButton')

        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon_path = str(self.__path) + '/static/control_button/plasma/'
        self.__symbolic = ''

        self.mouse_press_signal.connect(self.__on_click)
        self.application_frame_signal.connect(self.__on_application_frame)

    def __on_application_frame(self) -> None:
        dark = self._application_frame.style[
            '[FrameMaxButton]']['background_color']
        self.__symbolic = '-symbolic' if dark else ''
        self._application_frame.shape_signal.connect(self.__on_shape)
        # self._application_frame._obj.activeChanged.connect(self.__on_active)
        # self.window.visibilityChanged.connect(self.on_visibility_changed)

    def __on_click(self) -> None:
        if self._application_frame.shape == FrameShape.MAX:
            self._application_frame.shape = FrameShape.FRAME
        else:
            self._application_frame.shape = FrameShape.MAX

    def __on_shape(self) -> None:
        if self._application_frame.shape == FrameShape.MAX:
            self._application_frame.style['[FrameMaxButton]']['icon'] = (
                self.__icon_path + 'window-restore' + self.__symbolic + '.svg')

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
        if self._application_frame.shape == FrameShape.MIN:
            self._application_frame.shape = FrameShape.FRAME
        else:
            self._application_frame.shape = FrameShape.MIN

    def __str__(self) -> str:
        return "<class 'FrameMinButton'>"
