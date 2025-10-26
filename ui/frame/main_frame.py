#!/usr/bin/env python3
from ..ui import UI
from .frame import Frame
# from ...core.signal import Signal


class MainFrame(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        UI.__init__(self, name='MainFrame')
        # self._QtObject__name = 'MainFrame'

    def __repr__(self) -> str:
        return self.__class__.__name__
