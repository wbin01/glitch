#!/usr/bin/env python3
from PySide6.QtCore import QTimer

from ...enum.shape import Shape
from ..frame.frame import Frame


class Panel(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Panel', *args, **kwargs)
        self._UI__app = None

        self._app_signal.connect(self.__app_shape)

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> int:
        """..."""
        return int(self._QtObject__property('x'))

    @x.setter
    def x(self, x: int) -> None:
        self._QtObject__set_property('x', x)

    @property
    def y(self) -> int:
        """..."""
        return int(self._QtObject__property('y'))

    @y.setter
    def y(self, y: int) -> None:
        self._QtObject__set_property('y', y)

    def open(self) -> None:
        """..."""
        if self._QtObject__obj:
            self.height = int(self._app.height[0]) - 2
            self._QtObject__obj.open()

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(self.__update_size)

    def __update_size(self) -> None:
        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.height = int(self._app.height[0]) + 4
            self.x, self.y = -1, -1
        else:
            self.height = int(self._app.height[0]) - 2
            self.x, self.y = 0, 0
