#!/usr/bin/env python3
from .button import Button
from ...enum.frame_action import FrameAction
from ...enum.frame_shape import FrameShape


class FrameActionButton(Button):
    """Tool Button Element."""
    def __init__(
            self, frame_action: FrameAction = FrameAction.CLOSE,
            *args, **kwargs) -> None:
        super().__init__()
        # Args
        self.__frame_action = frame_action
        self.size = 22
        self.style_class = 'ActionButton'
        self.application_frame_signal.connect(self.__set_style)
        self.connect(self.__on_click)

    def __set_style(self) -> None:
        clean_style = {
            'border_color': '#00000000',
            'background_color': '#00000000',
            }
        self._application_frame.style['[ActionButton]'] = clean_style
        self._application_frame.style['[ActionButton:hover]'] = clean_style
        self._application_frame.style['[ActionButton:clicked]'] = clean_style

        self.icon = self.__get_icon()
        self._application_frame.shape_signal.connect(self.__update_icon)

    def __get_icon(self) -> str:
        if self.__frame_action == FrameAction.MAX:
            if self._application_frame.shape == FrameShape.MAX:
                return 'window-restore'
            return 'window-maximize'
        elif self.__frame_action == FrameAction.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                return 'window-restore'
            return 'view-fullscreen'
        elif self.__frame_action == FrameAction.MIN:
            return 'window-minimize'
        return 'window-close'

    def __on_click(self) -> None:
        if self.__frame_action == FrameAction.MAX:
            if self._application_frame.shape == FrameShape.MAX:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.MAX
        elif self.__frame_action == FrameAction.FULL:
            if self._application_frame.shape == FrameShape.FULL:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.FULL
        elif self.__frame_action == FrameAction.MIN:
            if self._application_frame.shape == FrameShape.MIN:
                self._application_frame.shape = FrameShape.FRAME
            else:
                self._application_frame.shape = FrameShape.MIN

        elif self.__frame_action == FrameAction.CLOSE:
            self._application_frame._obj.close()

    def __update_icon(self) -> str:
        self.icon = self.__get_icon()
