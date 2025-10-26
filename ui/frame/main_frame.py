#!/usr/bin/env python3
from ..ui import UI
from .frame import Frame
from ...core.signal import Signal


class MainFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        UI.__init__(self, name='MainFrame')
        self._UI__frame = self

    @property
    def _platform(self):
        """..."""
        return self.__platform

    @property
    def _platform_added_signal(self):
        """..."""
        return self.__platform_added_signal

    def __repr__(self) -> str:
        return self.__class__.__name__
