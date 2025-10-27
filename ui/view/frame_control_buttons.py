#!/usr/bin/env python3
from ..layout import Row
from .frame_close_button import FrameCloseButton
from .frame_max_button import FrameMaxButton
from .frame_min_button import FrameMinButton


class FrameControlButtons(Row):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__close_btn = self.add(FrameCloseButton())
        self.__max_btn = self.add(FrameMaxButton())
        self.__min_btn = self.add(FrameMinButton())
        self._QtObject__set_property('Layout.margins', 5)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'
