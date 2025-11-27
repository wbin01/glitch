#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...enum.anim import Anim


class Context(View):
    def __init__(
            self, width: int = 100, height: int = 100, push: bool = True,
            *args, **kwargs) -> None:
        super().__init__(name='Context', *args, **kwargs)
        self.__width = width
        self.__height = height
        self.__push = push

        self.visible = True
        self.width = self.__width
        self.height = self.__height
        # if self.__push:
        #     self.visible = False
        #     self._QtObject__set_property('width', self.__width)
        #     self._QtObject__set_property('height', self.__height)

        # self._QtObject__set_property('panelWidth', self.__width)
        # self._QtObject__set_property('panelHeight', self.__height)

        self.__obj = None
        self.__anim = None
        self.__close_conn = None
        self.__t_type = b'xScale'

        self._render_signal.connect(
            lambda: self._QtObject__set_property(
                'appParent', self._app._QtObject__obj.property('objectName')))

    @property
    def height(self) -> tuple:
        """..."""
        return self._QtObject__property('panelHeight')

    @height.setter
    def height(self, height: int | tuple) -> None:
        if isinstance(height, tuple):
            height = height[0]

        self._QtObject__set_property('panelHeight', height)
        if self.__push:
            self.visible = False
            self._QtObject__set_property('height', height)

    # @property
    # def visible(self) -> bool:
    #     """..."""
    #     return self.__get_visible()

    # @visible.setter
    # def visible(self, value: str) -> None:
    #     self.__set_visible(value)

    @property
    def width(self) -> tuple:
        """..."""
        return self._QtObject__property('panelWidth')

    @width.setter
    def width(self, width: int | tuple) -> None:
        if isinstance(width, tuple):
            width = width[0]

        self._QtObject__set_property('panelWidth', width)
        if self.__push:
            self.visible = False
            self._QtObject__set_property('width', width)

    @property
    def visible_panel(self) -> bool:
        """..."""
        return self._QtObject__property('panelVisible')

    @visible_panel.setter
    def visible_panel(self, visible_panel: bool) -> None:
        self.open() if visible_panel else self.close()

    def open(self) -> None:
        """..."""
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
        if self.__push: self.visible = True

        if not self.__anim:
            self.__anim = QtCore.QPropertyAnimation(self.__obj, self.__t_type)
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
            self.__anim = QtCore.QPropertyAnimation(self.__obj, self.__t_type)
            self.__anim.setDuration(100)

        self.__anim.setStartValue(1.0)
        self.__anim.setEndValue(0.0)
        self.__anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        
        self.__close_conn = self.__anim.finished.connect(self.__close)
        self.__anim.start()

    def __close(self) -> None:
        self._QtObject__set_property('panelVisible', False)
        if self.__push: self.visible = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
