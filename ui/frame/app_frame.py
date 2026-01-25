#!/usr/bin/env python3
from .main_frame import MainFrame
from ..ui import UI
from ..view.header import Header


class AppFrame(MainFrame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(movable=True, resizable=True, *args, **kwargs)
        self.header = self.add(Header(self._platform))

    def __repr__(self) -> str:
        return self.__class__.__name__
