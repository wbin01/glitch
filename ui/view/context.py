#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...enum.anim import Anim


class Context(View):
    """Simple context panel"""
    def __init__(
            self, animation: Anim = Anim.LEFT, panel: bool = False,
            x: int | None = None, y: int | None = None,
            *args, **kwargs) -> None:
        """
        panel:
            In panel mode (panel=True), the 'Layout' (Column/Row) includes 
            spacing, which causes a slight visual change. In this case, it is 
            recommended to add the Context at the end, especially if you are 
            using absolute positioning with `x` and `y`.

            In context mode (panel=False), which is the default, when the 
            layout is expanded, no displacement is perceived.

        x and y:
            The `x` and `y` arguments have no properties and need to be 
            defined when the instance is created, and they only work 
            in `panel` mode.

            If the x and y positions are configured, the `Context` positioning 
            will be absolute relative to the 'Layout' (Column/Row) in which it 
            was added.

        :param animation: `Anim` Enumeration (Enum).
        :param panel: `True` will make the `Context` behave like the `Panel`.
        :param x: Absolute horizontal position in relation to the 'Layout'.
        :param y: Absolute vertical position in relation to the 'Layout'.
        """
        super().__init__(name='Context', *args, **kwargs)
        self.__animation = animation
        self.__panel = panel
        self.__x = x
        self.__y = y
        self.__true_visible = False

        if self.__true_visible or not self.__panel:
            self._UI__set_visible(False)
        else:
            self._UI__set_visible(True if self.__panel else False)

        self.height = 50
        self.width = 50

        self.__tr = b'xScale'
        self.__scale_anim_time = 200
        self.__slide_anim_time = 200
        self.__fade_anim_time = 200
        self.__transition = True
        self.__static = False

        self.__obj = None
        self.__anim = None
        self.__close_conn = None

        self._app_signal.connect(self.__app_shape)
        self._render_signal.connect(self.__app_parent)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def height(self) -> tuple:
        """..."""
        height = self._QtObject__property('panelHeight')
        return height, height, height

    @height.setter
    def height(self, height: int | tuple) -> None:
        if isinstance(height, tuple):
            height = height[0]

        self._QtObject__set_property('panelHeight', height)
        if not self.__panel:
            self._QtObject__set_property('height', height)

    @property
    def visible(self) -> bool:
        """..."""
        return self._QtObject__property('panelVisible')

    @visible.setter
    def visible(self, visible: bool) -> None:
        self.open() if visible else self.close()

    @property
    def width(self) -> tuple:
        """..."""
        width = self._QtObject__property('panelWidth')
        return width, width, width

    @width.setter
    def width(self, width: int | tuple) -> None:
        if isinstance(width, tuple):
            width = width[0]

        self._QtObject__set_property('panelWidth', width)
        if not self.__panel:
            self._QtObject__set_property('width', width)

    def open(self, animation: Anim = None) -> None:
        """..."""
        if self.__panel:
            if self.__x is not None:
                self._QtObject__set_property('x', self.__x)
            if self.__y is not None:
                self._QtObject__set_property('y', self.__y)
        self.__anim_open(animation)

    def close(self) -> None:
        """..."""
        self.__anim_close()

    def __anim_open(self, animation: Anim = None) -> None:
        """..."""
        if not self.__obj:
            self.__obj = self._QtObject__obj.findChild(
                QtCore.QObject, 'scaleTransform')

        # Animation running
        if (self.__anim and
                self.__anim.state() == QtCore.QAbstractAnimation.Running):
            self.__anim.stop()

        if self.__close_conn:
            self.__anim.finished.disconnect(self.__close_conn)
            self.__close_conn = None

        self._QtObject__set_property('panelVisible', True)
        if self.__true_visible or not self.__panel:
            self._UI__set_visible(True)

        # Animation
        if animation: self.__animation = animation
        slide_time = 0 if not self.__transition else self.__slide_anim_time
        scale_time = 0 if not self.__transition else self.__scale_anim_time

        self._QtObject__set_property('originX', 0)
        self._QtObject__set_property('originY', 0)
        center_scale = False

        if self.__animation == Anim.LEFT:
            self._QtObject__set_property('originX', 0)
        elif self.__animation == Anim.RIGHT:
            self._QtObject__set_property('originX', self.width[0])
        elif self.__animation == Anim.TOP:
            self._QtObject__set_property('originY', 0)
        elif self.__animation == Anim.BOTTOM:
            self._QtObject__set_property('originY', self.height[0])
        elif self.__animation == Anim.CENTER:
            self._QtObject__set_property('originX', self.width[0] // 2)
            self._QtObject__set_property('originY', self.height[0] // 2)
            center_scale = True

        ani = self.__animation.value
        self.__tr = b'xScale' if 'LEFT' in ani or 'RIGHT' in ani else b'yScale'

        self.__anim = QtCore.QParallelAnimationGroup()

        scale_in = QtCore.QPropertyAnimation(self.__obj, self.__tr)
        scale_in.setDuration(100)
        scale_in.setStartValue(0.0)
        scale_in.setEndValue(1.0)
        scale_in.setEasingCurve(QtCore.QEasingCurve.OutCubic)
        self.__anim.addAnimation(scale_in)

        if center_scale:
            scale_on = QtCore.QPropertyAnimation(self.__obj, b'xScale')
            scale_on.setDuration(100)
            scale_on.setStartValue(0.0)
            scale_on.setEndValue(1.0)
            scale_on.setEasingCurve(QtCore.QEasingCurve.OutCubic)
            self.__anim.addAnimation(scale_on)

        self.__anim.start()

    def __anim_close(self) -> None:
        if not self.__obj:
            self.__obj = self._QtObject__obj.findChild(
                QtCore.QObject, 'scaleTransform')

        # Animation running
        # if (self.__anim
        #         and self.__anim.state() == QtCore.QAbstractAnimation.Running):
        #     self.__anim.stop()
        self.__close()
        self.__close_conn = self.__anim.finished.connect(self.__close)
        # self.__anim.start()

    def __app_parent(self):
        self._QtObject__set_property(
            'appParent', self._app._QtObject__obj.property('objectName'))

    def __app_shape(self) -> None:
        self._app._shape_signal.connect(self.__close)

    def __close(self) -> None:
        self._QtObject__set_property('panelVisible', False)

        if self.__true_visible or not self.__panel:
            self._UI__set_visible(False)
