#!/usr/bin/env python3
from ..ui import UI
from .frame import Frame
from ...core.signal import Signal


class AppFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        UI.__init__(self, name='AppFrame')
        self.__render_signal = Signal()
        self.__resize_signal = Signal()
        self.__state_signal = Signal()
        self._UI__app = self

    @property
    def _render_signal(self):
        """..."""
        return self.__render_signal

    @property
    def _state_signal(self):
        """..."""
        return self.__state_signal

    def __repr__(self) -> str:
        return self.__class__.__name__
