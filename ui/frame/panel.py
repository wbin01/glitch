#!/usr/bin/env python3
from PySide6 import QtCore

from ...enum.shape import Shape
from ...enum.animation import Animation
from ..frame.frame import Frame


class Panel(Frame):
    """..."""
    def __init__(
            self, animation: Animation = Animation.FROM_LEFT,
            *args, **kwargs) -> None:
        super().__init__(name='Panel', *args, **kwargs)
        """
        transformOrigin: 
        Item.Top Item.Bottom Item.Right Item.Left
        """
        self._UI__app = None

        self.__animation = animation
        self.__fy = 0
        self.__fx = 0
        self.__w = None
        self.__h = None
        self.__anim = None
        
        self._app_signal.connect(self.__app_shape)

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def animation(self) -> int:
        """..."""
        return self.__animation

    @animation.setter
    def animation(self, animation: int) -> None:
        self.__animation = animation

    @property
    def floating(self) -> int:
        """..."""
        return self.__fx

    @floating.setter
    def floating(self, floating: int) -> None:
        self.__fx, self.__fy = floating, floating

    @property
    def size(self) -> tuple:
        """Min is 100 (auto)"""
        return self.__w, self.__h

    @size.setter
    def size(self, size: int | tuple = None) -> None:
        if size is None:
            return

        if isinstance(size, int):
            self.__w = size

        elif isinstance(size, tuple):
            if not size:
                return

            elif len(size) == 1:
                self.__w = size[0]
            else:
                self.__w, self.__h = size[:2]

    def open(self) -> None:
        """..."""
        if not self._QtObject__obj or not self._app:
            return

        if self.__animation == Animation.FROM_LEFT:
            start, end = self.__anim_from_left()
        elif self.__animation == Animation.FROM_RIGHT:
            start, end = self.__anim_from_right()
        elif self.__animation == Animation.FROM_TOP:
            start, end = self.__anim_from_top()
        else:
            start, end = self.__anim_from_bottom()

        self._QtObject__obj.open()

        anim_type = b'x' if (self.__animation == Animation.FROM_LEFT or
            self.__animation == Animation.FROM_RIGHT) else b'y'

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

    def __anim_from_left(self) -> tuple:
        height = int(self._app.height[0]) if self.__h is None else self.__h
        self.width = 300 if self.__w is None else self.__w

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.height = height + 4 - (self.__fy * 2)
            self._QtObject__set_property('y', self.__fy - 1)
            end = self.__fx - 1
        else:
            self.height = height - 2 - (self.__fy * 2)
            self._QtObject__set_property('y', self.__fy)
            end = self.__fx

        return -self.width[0], end

    def __anim_from_right(self) -> tuple:
        height = int(self._app.height[0]) if self.__h is None else self.__h
        app_width = int(self._app.width[0])
        self.width = 300 if self.__w is None else self.__w

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.height = height + 4 - (self.__fy * 2)
            self._QtObject__set_property('y', self.__fy - 1)
            end = app_width - ((self.width[0] + 1) + self.__fx)
        else:
            self.height = height - 2 - (self.__fy * 2)
            self._QtObject__set_property('y', self.__fy)
            end = app_width - ((self.width[0] + 2) + self.__fx)

        return app_width, end

    def __anim_from_top(self) -> tuple:
        app_height = int(self._app.height[0])
        width = int(self._app.width[0]) if self.__w is None else self.__w
        self.height = 300 if self.__h is None else self.__h

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.width = width - (self.__fx * 2)
            self._QtObject__set_property('x', self.__fx - 1)
            end = self.__fy - 1
        else:
            self.width = width - 2 - (self.__fx * 2)
            self._QtObject__set_property('x', self.__fx)
            end = self.__fy

        return -app_height, end

    def __anim_from_bottom(self) -> tuple:
        width = int(self._app.width[0]) if self.__w is None else self.__w
        app_height = int(self._app.height[0])
        self.height = 300 if self.__h is None else self.__h

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.width = width - (self.__fx * 2)
            self._QtObject__set_property('x', self.__fx - 1)
            end = app_height - ((self.height[0] + 1) + self.__fy)
        else:
            self.width = width - 2 - (self.__fx * 2)
            self._QtObject__set_property('x', self.__fx)
            end = app_height - ((self.height[0] + 2) + self.__fy)

        return app_height, end

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(lambda: self._QtObject__obj.close())
