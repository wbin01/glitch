#!/usr/bin/env python3
from PySide6.QtCore import QTimer

from ..ui import UI
from ..mixin.add import Add
from ..frame.frame import Frame


class Panel(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Panel', *args, **kwargs)
        self._UI__app = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    def open(self) -> None:
        """..."""
        if self._QtObject__obj:
            self.height = int(self._app.height[0]) - 2
            self._QtObject__obj.open()
