#!/usr/bin/env python3
import pathlib

from .button import Button
from ...core.application_style import style_value
from ...enum.frame_control import FrameControl
from ...enum.frame_shape import FrameShape
from ...enum.event import Event
from ...tools import color_converter


class FrameControlButton(Button):
    """Tool Button Element."""
    def __init__(
            self, frame_action: FrameControl = FrameControl.CLOSE,
            *args, **kwargs) -> None:
        super().__init__()
        # Args
        self.__frame_action = frame_action

        # Properties
        self.__path = pathlib.Path(__file__).parent.parent.parent
        self.__icon_path = str(self.__path) + '/static/control_button/plasma/'
        self.__is_dark = False
        self.__symbolic = '-symbolic' if self.__is_dark else ''
        self.__state = ''
        self.__plasma_close_button_with_circle = False

        # Set
        self.size = 22
        self.style_class = 'ActionButton'
        self.application_frame_signal.connect(self.__set_style)
        self.mouse_press_signal.connect(self.__on_click)
        self.mouse_hover_signal.connect(self.__on_hover)

    def __set_style(self) -> None:
        header = '[' + self._application_frame._name + ']'
        inactive_header = '[' + self._application_frame._name + ':inactive]'
        propert = 'background_color'
        style = {
            'border_color': '#00000000',
            'background_color': header + propert}

        self._application_frame.style['[ActionButton]'] = style
        self._application_frame.style['[ActionButton:hover]'] = style
        self._application_frame.style['[ActionButton:clicked]'] = style
        self._application_frame.style['[ActionButton:inactive]'] = {
            'border_color': '#00000000',
            'background_color': inactive_header + propert}

        self.__is_dark = color_converter.is_dark(color_converter.hex_to_rgba(
            style_value(self._application_frame.style, header, propert)))
        self.__symbolic = '-symbolic' if self.__is_dark else ''

        self.icon = self.__get_icon()
        self._application_frame.shape_signal.connect(self.__update_icon)

    def __get_icon(self) -> str:
        return self.__get_plasma_icon()

    def __get_plasma_icon(self) -> str:
        state = self.__state + self.__symbolic

        if self.__frame_action == FrameControl.MAX:
            if (self._application_frame.shape == FrameShape.MAX or
                    self._application_frame.shape == FrameShape.FULL):
                return self.__icon_path + 'window-restore' + state + '.svg'
            return self.__icon_path + 'go-up' + state + '.svg'
        elif self.__frame_action == FrameControl.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                return self.__icon_path + 'window-restore' + state + '.svg'
            return self.__icon_path + 'view-fullscreen' + state + '.svg'
        elif self.__frame_action == FrameControl.MIN:
            return self.__icon_path + 'go-down' + state + '.svg'

        if self.__plasma_close_button_with_circle:
            return self.__icon_path + 'window-close' + state + '.svg'
        else:
            name = 'window-close-b'
            if self.__state == '-hover':
                name = 'window-close'
                if not self._application_frame._obj.isActive():
                    state = ''
            return self.__icon_path + name + state + '.svg'

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

    def __on_hover(self, *args) -> None:
        self.__state = '-hover' if self.is_mouse_hover() else ''
        self.__update_icon()

    def __update_icon(self) -> str:
        self.icon = self.__get_icon()
