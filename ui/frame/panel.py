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
        self.__fy = 0
        self.__fx = 0
        self.__width = 300
        self.__float = True
        self.__side = 0
        self.__size = 300

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def x(self) -> int:
        """..."""
        return self.__fx

    @x.setter
    def x(self, x: int) -> None:
        self.__fx = x

    @property
    def y(self) -> int:
        """..."""
        return self.__fy

    @y.setter
    def y(self, y: int) -> None:
        self.__fy = y

    def open(self, side=2) -> None:
        """..."""
        self.__side = side
        fy = (self.__fy * 2 if self.__float else self.__fy)
        fx = (self.__fx * 2 if self.__float else self.__fx)
        height = int(self._app.height[0])
        width = int(self._app.width[0])

        if self._QtObject__obj and self.__side == 0 or self.__side == 1:
            anim_type = b'x'
            self.width = self.__size
            if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
                self.height = height + 4 - fy
                self._QtObject__set_property('y', self.__fy - 1)
                size = (self.__size + 1) + self.__fx
                end = self.__fx - 1 if self.__side == 0 else width - size
            else:
                self.height = height - 2 - fy
                self._QtObject__set_property('y', self.__fy)
                size = (self.__size + 2) + self.__fx
                end = self.__fx if self.__side == 0 else width - size

            start = -self.__size if self.__side == 0 else width + self.__size

        if self._QtObject__obj and self.__side == 2 or self.__side == 3:
            anim_type = b'y'
            self.height = self.__size
            if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
                self.width = width - fx
                self._QtObject__set_property('x', self.__fx - 1)

                size = (self.__size + 1) + self.__fy
                end = self.__fy - 1 if self.__side == 2 else height - size
            else:
                self.width = width - 2 - fx
                self._QtObject__set_property('x', self.__fx)
                size = (self.__size + 2) + self.__fy
                end = self.__fy if self.__side == 2 else height - size


            start = -self.__size if self.__side == 2 else height

        self._QtObject__obj.open()

        self.__anim = None
        slide_in = QtCore.QPropertyAnimation(self._QtObject__obj, anim_type)
        slide_in.setDuration(300)
        slide_in.setStartValue(start)
        slide_in.setEndValue(end)
        slide_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        fade_in = QtCore.QPropertyAnimation(self._QtObject__obj, b'opacity')
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
