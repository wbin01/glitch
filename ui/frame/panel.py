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
        self.__slide_anim_time = 200
        self.__fade_anim_time = 200
        self.__transition = True
        self.__static = False

        self.__anim = None
        self._app_signal.connect(self.__app_shape)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(animation={self.__animation!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__animation!r})'

    @property
    def animation(self) -> int:
        """..."""
        return self.__animation

    @animation.setter
    def animation(self, animation: int) -> None:
        self.__animation = animation

    @property
    def height(self) -> int:
        """
        None is auto:
            Left and right is 300-width and app-height.
            Top and bottom is app-width and 300-height.
        """
        return self.__h

    @height.setter
    def height(self, height: int | tuple) -> None:
        if isinstance(height, tuple):
            height = height[0]

        h = None
        if isinstance(height, int):
            h = height

        elif isinstance(height, tuple):
            if not height:
                return
            h = height[0]

        if isinstance(h, int) or h is None: self.__h = h

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
    def static(self) -> bool:
        """..."""
        return self.__static

    @static.setter
    def static(self, static: bool) -> None:
        # 0 Popup.NoAutoClose, 1: Popup.autoClose
        self.__static = static
        self._QtObject__set_property('closePolicy', 0 if static else 1)

    @property
    def transition(self) -> bool:
        return self.__transition

    @transition.setter
    def transition(self, transition: bool) -> None:
        self.__transition = transition

    @property
    def width(self) -> int:
        """
        None is auto:
            Left and right is 300-width and app-height.
            Top and bottom is app-width and 300-height.
        """
        return self.__w

    @width.setter
    def width(self, width: int | tuple) -> None:
        if isinstance(width, tuple):
            width = width[0]

        w = None
        if isinstance(width, int):
            w = width

        elif isinstance(width, tuple):
            if not width:
                return
            w = width[0]

        if isinstance(w, int) or w is None: self.__w = w

    def open(self, animation: Anim = None) -> None:
        """..."""
        if not self._QtObject__obj or not self._app:
            return

        if (self.__anim and
                self.__anim.state() == QtCore.QAbstractAnimation.Running):
            self.__anim.stop()

        if animation: self.__animation = animation
        slide_time = 0 if not self.__transition else self.__slide_anim_time

        if self.__animation == Anim.CENTER:
            return

        if self.__animation == Anim.LEFT:
            start, end = self.__anim_left()
        elif self.__animation == Anim.RIGHT:
            start, end = self.__anim_right()
        elif self.__animation == Anim.TOP:
            start, end = self.__anim_top()
        elif self.__animation == Anim.BOTTOM:
            start, end = self.__anim_bottom()

        self._QtObject__obj.open()

        value = self.__animation.value
        anim_type = b'x' if 'LEFT' in value or 'RIGHT' in value else b'y'

        self.__anim = QtCore.QParallelAnimationGroup()
        
        slide_in = QtCore.QPropertyAnimation(self._QtObject__obj, anim_type)
        slide_in.setDuration(slide_time)
        slide_in.setStartValue(start)
        slide_in.setEndValue(end)
        slide_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.__anim.addAnimation(slide_in)

        fade_in = QtCore.QPropertyAnimation(self._QtObject__obj, b'opacity')
        fade_in.setDuration(self.__fade_anim_time)
        fade_in.setStartValue(0)
        fade_in.setEndValue(1)
        fade_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.__anim.addAnimation(fade_in)

        self.__anim.start()

    def reset(
            self,
            animation: Anim = Anim.LEFT,
            width: int = None,
            height: int = None,
            margin: tuple = 0,
            static: bool = False,
            transition: bool = True
            ) -> None:
        """..."""
        self.animation = animation
        self.width = width
        self.height = height
        self.margin = margin
        self.static = static
        self.transition = transition

    def __anim_top(self) -> tuple:
        app_height = self._app.height[0]
        width = self._app.width[0] if self.__w is None else self.__w
        self._UI__set_height(300 if self.__h is None else self.__h)

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self._UI__set_width(width - (self.__ml + self.__mr))
            self._QtObject__set_property('x', self.__ml - 1)
            end = -1
        else:
            # self._UI__set_width((width - 2) - (self.__ml + self.__mr))
            # self._QtObject__set_property('x', self.__ml)
            # end = 0
            self._UI__set_width(width - (self.__ml + self.__mr))
            self._QtObject__set_property('x', self.__ml - 1)
            end = -1

        return -app_height, end + self.__mt

    def __anim_right(self) -> tuple:
        height = self._app.height[0] if self.__h is None else self.__h
        app_width = self._app.width[0]
        self._UI__set_width(300 if self.__w is None else self.__w)

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self._UI__set_height((height + 2) - (self.__mt + self.__mb))
            self._QtObject__set_property('y', self.__mt - 1)
            end = app_width - (self._UI__get_width()[0] + 1)
        else:
            # self._UI__set_height((height - 2) - (self.__mt + self.__mb))
            # self._QtObject__set_property('y', self.__mt)
            # end = app_width - (self._UI__get_width()[0] + 2)
            self._UI__set_height(height - (self.__mt + self.__mb))
            self._QtObject__set_property('y', self.__mt - 1)
            end = app_width - (self._UI__get_width()[0] + 1)

        return app_width, end - self.__mr

    def __anim_bottom(self) -> tuple:
        width = self._app.width[0] if self.__w is None else self.__w
        app_height = self._app.height[0]
        self._UI__set_height(300 if self.__h is None else self.__h)

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self._UI__set_width(width - (self.__ml + self.__mr))
            self._QtObject__set_property('x', self.__ml - 1)
            end = app_height - (self._UI__get_height()[0] + 1)
        else:
            # self._UI__set_width((width - 2) - (self.__ml + self.__mr))
            # self._QtObject__set_property('x', self.__ml)
            # end = app_height - (self._UI__get_height()[0] + 2)
            self._UI__set_width(width - (self.__ml + self.__mr))
            self._QtObject__set_property('x', self.__ml - 1)
            end = app_height - (self._UI__get_height()[0] + 1)

        return app_height, end - self.__mb

    def __anim_left(self) -> tuple:
        height = self._app.height[0] if self.__h is None else self.__h
        self._UI__set_width(300 if self.__w is None else self.__w)

        if self._app.shape == Shape.MAX or self._app.shape == Shape.FULL:
            self._UI__set_height((height + 2) - (self.__mt + self.__mb))
            self._QtObject__set_property('y', self.__mt - 1)
            end = -1
        else:
            # self._UI__set_height((height - 2) - (self.__mt + self.__mb))
            # self._QtObject__set_property('y', self.__mt)
            # end = 0
            self._UI__set_height(height - (self.__mt + self.__mb))
            self._QtObject__set_property('y', self.__mt - 1)
            end = -1

        return -self._UI__get_width()[0], end + self.__ml

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(lambda: self._QtObject__obj.close())
