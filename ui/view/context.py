#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...enum.anim import Anim


class Context(View):
    def __init__(
            self, x: int = 0, y: int = 0, panel: bool = False,
            *args, **kwargs) -> None:
        super().__init__(name='Context', *args, **kwargs)
        self.__x = x
        self.__y = y
        self.__panel = panel

        self._UI__set_visible(True if self.__panel else False)
        self.height = 50
        self.width = 50

        self.__obj = None
        self.__anim = None
        self.__close_conn = None
        self.__tr = b'xScale'

        self._render_signal.connect(self.__app_parent)

    def __app_parent(self):
        self._QtObject__set_property(
            'appParent', self._app._QtObject__obj.property('objectName'))

    @property
    def height(self) -> tuple:
        """..."""
        return self._QtObject__property('panelHeight')

    @height.setter
    def height(self, height: int | tuple) -> None:
        if isinstance(height, tuple):
            height = height[0]

        self._QtObject__set_property('panelHeight', height)
        if not self.__panel:
            self._QtObject__set_property('height', height)

    @property
    def width(self) -> tuple:
        """..."""
        return self._QtObject__property('panelWidth')

    @width.setter
    def width(self, width: int | tuple) -> None:
        if isinstance(width, tuple):
            width = width[0]

        self._QtObject__set_property('panelWidth', width)
        if not self.__panel:
            self._QtObject__set_property('width', width)

    @property
    def visible(self) -> bool:
        """..."""
        return self._QtObject__property('panelVisible')

    @visible.setter
    def visible(self, visible: bool) -> None:
        self.open() if visible else self.close()

    def open(self) -> None:
        """..."""
        self._QtObject__set_property('x', self.__x)
        self._QtObject__set_property('y', self.__y)
        self.__anim_open()

    def close(self) -> None:
        """..."""
        self.__anim_close()

    def __anim_open(self) -> None:
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

        # Animation
        self._QtObject__set_property('panelVisible', True)
        if not self.__panel: self._UI__set_visible(True)

        if not self.__anim:
            self.__anim = QtCore.QPropertyAnimation(self.__obj, self.__tr)
            self.__anim.setDuration(100)

        self.__anim.setStartValue(0.0)
        self.__anim.setEndValue(1.0)
        self.__anim.start()

    def __anim_close(self) -> None:
        if not self.__obj:
            self.__obj = self._QtObject__obj.findChild(
                QtCore.QObject, 'scaleTransform')

        # Animation running
        if (self.__anim
                and self.__anim.state() == QtCore.QAbstractAnimation.Running):
            self.__anim.stop()

        # Animation
        if not self.__anim:
            self.__anim = QtCore.QPropertyAnimation(self.__obj, self.__tr)
            self.__anim.setDuration(100)

        self.__anim.setStartValue(1.0)
        self.__anim.setEndValue(0.0)
        self.__anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        
        self.__close_conn = self.__anim.finished.connect(self.__close)
        self.__anim.start()

    def __close(self) -> None:
        self._QtObject__set_property('panelVisible', False)
        if not self.__panel: self._UI__set_visible(False)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
