#!/usr/bin/env python3
import logging

from .mixin import MarginsMixin, SizeMixin
from .ui import UI
from ...core.signal import Signal
# from ...enum import Size


class Element(MarginsMixin, SizeMixin, UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.size_signal = Signal()

        # self.__fill_height = False
        # self.__fill_width = True
        self.class_id('Element')

    def __str__(self) -> str:
        return "<class 'Element'>"
