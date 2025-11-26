#!/usr/bin/env python3
from PySide6 import QtCore

from ...enum.shape import Shape
from ...enum.anim import Anim
from ..frame.frame import Frame


class Panel(Frame):
    """..."""
    def __init__(self, animation: Anim = Anim.LEFT, *args, **kwargs) -> None:
        super().__init__(name='Panel', *args, **kwargs)
        """
        transformOrigin: 
        Item.Top Item.Bottom Item.Right Item.Left
        """
        self._UI__app = None

        self.__animation = animation
        self.__w = None
        self.__h = None
        self.__mt = 0
        self.__mr = 0
        self.__mb = 0
        self.__ml = 0
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
    def margin(self) -> tuple:
        """..."""
        return self.__mt, self.__mr, self.__mb, self.__ml

    @margin.setter
    def margin(self, margin: int | tuple = None) -> None:
        if margin is None:
            return

        mt, mr, mb, ml = None, None, None, None
        if isinstance(margin, int):
            mt, mr, mb, ml = margin, margin, margin, margin

        elif isinstance(margin, tuple):
            if not margin:
                return

            elif len(margin) == 1:
                mt = margin[0]
            elif len(margin) == 2:
                mt, mr = margin
            elif len(margin) == 3:
                mt, mr, mb = margin
            else:
                mt, mr, mb, ml = margin[:4]

        if isinstance(mt, int): self.__mt = mt
        if isinstance(mr, int): self.__mr = mr
        if isinstance(mb, int): self.__mb = mb
        if isinstance(ml, int): self.__ml = ml

    @property
    def size(self) -> tuple:
        """
        None is auto:
            Left and right is 300-width and app-height.
            Top and bottom is app-width and 300-height.
        """
        return self.__w, self.__h

    @size.setter
    def size(self, size: int | tuple = None) -> None:
        if size is None:
            return

        w, h = None, None
        if isinstance(size, int):
            w = size

        elif isinstance(size, tuple):
            if not size:
                return

            elif len(size) == 1:
                w = size[0]
            else:
                w, h = size[:2]

        if isinstance(w, int) or w is None: self.__w = w
        if isinstance(h, int) or h is None: self.__h = h

    def open(self, animation: Anim = None) -> None:
        """..."""
        if not self._QtObject__obj or not self._app:
            return

        if animation: self.__animation = animation

        scale = False
        if self.__animation == Anim.LEFT:
            start, end = self.__anim_left()
        elif self.__animation == Anim.RIGHT:
            start, end = self.__anim_right()
        elif self.__animation == Anim.TOP:
            start, end = self.__anim_top()
        elif self.__animation == Anim.BOTTOM:
            start, end = self.__anim_bottom()
        elif self.__animation == Anim.CENTER:
            scale = self.__anim_center()
        elif self.__animation == Anim.CENTER_FROM_TOP:
            start, end = self.__anim_center_from_top()
        elif self.__animation == Anim.CENTER_FROM_RIGHT:
            start, end = self.__anim_center_from_right()
        elif self.__animation == Anim.CENTER_FROM_BOTTOM:
            start, end = self.__anim_center_from_bottom()
        elif self.__animation == Anim.CENTER_FROM_LEFT:
            start, end = self.__anim_center_from_left()

        self._QtObject__obj.open()

        value = self.__animation.value
        anim_type = b'x' if 'LEFT' in value or 'RIGHT' in value else b'y'

        self.__anim = None
        self.__anim = QtCore.QParallelAnimationGroup()
        
        if scale:
            scale = QtCore.QPropertyAnimation(self._QtObject__obj, b'scale')
            scale.setDuration(300)
            scale.setStartValue(0.0)
            scale.setEndValue(1.0)
            scale.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.__anim.addAnimation(scale)
        else:
            slide_in = QtCore.QPropertyAnimation(self._QtObject__obj, anim_type)
            slide_in.setDuration(300)
            slide_in.setStartValue(start)
            slide_in.setEndValue(end)
            slide_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.__anim.addAnimation(slide_in)

        fade_in = QtCore.QPropertyAnimation(self._QtObject__obj, b'opacity')
        fade_in.setDuration(300)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.__anim.addAnimation(fade_in)

        self.__anim.start()

    def __anim_top(self) -> tuple:
        app_height = self._app.height[0]
        width = self._app.width[0] if self.__w is None else self.__w
        self.height = 300 if self.__h is None else self.__h

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.width = width - (self.__ml + self.__mr)
            self._QtObject__set_property('x', self.__ml - 1)
            end = -1
        else:
            self.width = (width - 2) - (self.__ml + self.__mr)
            self._QtObject__set_property('x', self.__ml)
            end = 0

        return -app_height, end + self.__mt

    def __anim_right(self) -> tuple:
        height = self._app.height[0] if self.__h is None else self.__h
        app_width = self._app.width[0]
        self.width = 300 if self.__w is None else self.__w

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.height = (height + 2) - (self.__mt + self.__mb)
            self._QtObject__set_property('y', self.__mt - 1)
            end = app_width - (self.width[0] + 1)
        else:
            self.height = (height - 2) - (self.__mt + self.__mb)
            self._QtObject__set_property('y', self.__mt)
            end = app_width - (self.width[0] + 2)

        return app_width, end - self.__mr

    def __anim_bottom(self) -> tuple:
        width = self._app.width[0] if self.__w is None else self.__w
        app_height = self._app.height[0]
        self.height = 300 if self.__h is None else self.__h

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.width = width - (self.__ml + self.__mr)
            self._QtObject__set_property('x', self.__ml - 1)
            end = app_height - (self.height[0] + 1)
        else:
            self.width = (width - 2) - (self.__ml + self.__mr)
            self._QtObject__set_property('x', self.__ml)
            end = app_height - (self.height[0] + 2)

        return app_height, end - self.__mb

    def __anim_left(self) -> tuple:
        height = self._app.height[0] if self.__h is None else self.__h
        self.width = 300 if self.__w is None else self.__w

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self.height = (height + 2) - (self.__mt + self.__mb)
            self._QtObject__set_property('y', self.__mt - 1)
            end = -1
        else:
            self.height = (height - 2) - (self.__mt + self.__mb)
            self._QtObject__set_property('y', self.__mt)
            end = 0

        return -self.width[0], end + self.__ml

    def __anim_center(self) -> bool:
        app_height = self._app.height[0]
        app_width = self._app.width[0]

        width = 300 if self.__w is None else self.__w
        self.width = width
        
        height = 300 if self.__h is None else self.__h
        self.height = height

        y = (app_height // 2) - (height // 2)
        if self.__mt > self.__mb: y = y + (self.__mt - self.__mb)
        if self.__mb > self.__mt: y = y - (self.__mb - self.__mt)

        x = (app_width // 2) - (width // 2)
        if self.__ml > self.__mr: x = x + (self.__ml - self.__mr)
        if self.__mr > self.__ml: x = x - (self.__mr - self.__ml)

        self._QtObject__set_property('x', x)
        self._QtObject__set_property('y', y)

        return True

    def __anim_center_from_top(self) -> tuple:
        app_height = self._app.height[0]
        app_width = self._app.width[0]

        width = 300 if self.__w is None else self.__w
        self.height = 300 if self.__h is None else self.__h
        self.width = width

        self._QtObject__set_property('x', (app_width // 2) - (width // 2))

        return -app_height, (app_height // 2) - (self.height[0] // 2)

    def __anim_center_from_right(self) -> tuple:
        app_height = self._app.height[0]
        app_width = self._app.width[0]

        self.width = 300 if self.__w is None else self.__w
        height = 300 if self.__h is None else self.__h
        self.height = height
        
        self._QtObject__set_property('y', (app_height // 2) - (height // 2))

        return app_width, (app_width // 2) - (self.width[0] // 2)

    def __anim_center_from_bottom(self) -> tuple:
        app_height = self._app.height[0]
        app_width = self._app.width[0]

        width = 300 if self.__w is None else self.__w
        self.width = width
        self.height = 300 if self.__h is None else self.__h
        
        self._QtObject__set_property('x', (app_width // 2) - (width // 2))

        return app_height, (app_height // 2) - self.height[0] // 2

    def __anim_center_from_left(self) -> tuple:
        app_height = self._app.height[0]
        app_width = self._app.width[0]

        height = 300 if self.__h is None else self.__h
        self.width = 300 if self.__w is None else self.__w
        self.height = height

        self._QtObject__set_property('y', (app_height // 2) - (height // 2))

        return -self.width[0], (app_width // 2) - (self.width[0] // 2)

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(lambda: self._QtObject__obj.close())
