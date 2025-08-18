#!/usr/bin/env python3
import pathlib

from .button import Button
from ...core.application_style import style_value
from ...enum.frame_control import FrameControl
from ...enum.frame_shape import FrameShape
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

        # Set
        self.size = 22
        self.style_class = 'ActionButton'
        self.application_frame_signal.connect(self.__set_style)
        self.connect(self.__on_click)

    def __set_style(self) -> None:
        header = '[' + self._application_frame._name + ']'
        inactive_header = '[' + self._application_frame._name + ':inactive]'
        propert = 'background_color'
        clean_style = {
            'border_color': '#00000000',
            'background_color': header + propert}

        self._application_frame.style['[ActionButton]'] = clean_style
        self._application_frame.style['[ActionButton:hover]'] = clean_style
        self._application_frame.style['[ActionButton:clicked]'] = clean_style
        self._application_frame.style['[ActionButton:inactive]'] = {
            'border_color': '#00000000',
            'background_color': inactive_header + propert}

        # self.__is_dark = color_converter.is_dark(
        #     QtGui.QPalette().color(QtGui.QPalette.Window).toTuple())

        self.__is_dark = color_converter.is_dark(color_converter.hex_to_rgba(
            style_value(self._application_frame.style, header, propert)))
        self.__symbolic = '-symbolic' if self.__is_dark else ''

        self.icon = self.__get_icon()
        self._application_frame.shape_signal.connect(self.__update_icon)

    def __get_icon(self) -> str:
        return self.__get_plasma_icon()

    def __get_frame_icon(self) -> str:
        if self.__frame_action == FrameControl.MAX:
            if self._application_frame.shape == FrameShape.MAX:
                return 'window-restore'
            return 'window-maximize'
        elif self.__frame_action == FrameControl.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                return 'window-restore'
            return 'view-fullscreen'
        elif self.__frame_action == FrameControl.MIN:
            return 'window-minimize'
        return 'window-close'

    def __get_plasma_icon(self) -> str:
        state = self.__state + self.__symbolic

        if self.__frame_action == FrameControl.MAX:
            if self._application_frame.shape == FrameShape.MAX:
                return self.__icon_path + 'window-restore' + state + '.svg'
            return self.__icon_path + 'go-up' + state + '.svg'
        elif self.__frame_action == FrameControl.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                return self.__icon_path + 'window-restore' + state + '.svg'
            return self.__icon_path + 'view-fullscreen' + state + '.svg'
        elif self.__frame_action == FrameControl.MIN:
            return self.__icon_path + 'go-down' + state + '.svg'
        return self.__icon_path + 'window-close-b' + state + '.svg'

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

    def __update_icon(self) -> str:
        self.icon = self.__get_icon()
