#!/usr/bin/env python3
from PySide6 import QtCore

from ...enum.shape import Shape
from ..frame.frame import Frame


class Panel(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='Panel', *args, **kwargs)
        """
        transformOrigin: 
        Item.Top Item.Bottom Item.Right Item.Left
        """
        self._UI__app = None

        self._app_signal.connect(self.__app_shape)
        self.__anim = None
        self.__y = 0
        self.__x = 0
        self.__width = 300
        self.__float_width = False
        self.__float_height = True

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> int:
        """..."""
        return self.__x

    @x.setter
    def x(self, x: int) -> None:
        self.__x = x

    @property
    def y(self) -> int:
        """..."""
        return self.__y

    @y.setter
    def y(self, y: int) -> None:
        self.__y = y

    def open(self, side=1) -> None:
        """..."""
        height = (self.__y * 2 if self.__float_height else self.__y)
        # width = (self.__x * 2 if self.__float_width else self.__x)
        if self._QtObject__obj:
            self._QtObject__obj.open()
            if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
                self.height = int(self._app.height[0]) + 4 - height
                self._QtObject__set_property('y', self.__y - 1)
                end = self.__x - 1 if side == 0 else self._app.width[0] - 301 - self.__x
            else:
                self.height = int(self._app.height[0]) - 2 - height
                self._QtObject__set_property('y', self.__y)
                end = self.__x if side == 0 else self._app.width[0] - 302 - self.__x

            start = -300 if side == 0 else self._app.width[0] + 300
            self.__anim = None
            slide_in = QtCore.QPropertyAnimation(self._QtObject__obj, b"x")
            slide_in.setDuration(300)
            slide_in.setStartValue(start)
            slide_in.setEndValue(end)
            slide_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            fade_in = QtCore.QPropertyAnimation(self._QtObject__obj, b"opacity")
            fade_in.setDuration(300)
            fade_in.setStartValue(0)
            fade_in.setEndValue(1)
            fade_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.__anim = QtCore.QParallelAnimationGroup()
            self.__anim.addAnimation(slide_in)
            self.__anim.addAnimation(fade_in)
            self.__anim.start()

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(lambda: self._QtObject__obj.close())
