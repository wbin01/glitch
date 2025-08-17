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

        # Get sys
        self.style_class = 'ActionButton'
        self.application_frame_signal.connect(self.__set_style)

        # Set from sys
        self.size = self.size[1], self.size[1]

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

    def __update_icon(self) -> str:
        self.icon = self.__get_icon()

