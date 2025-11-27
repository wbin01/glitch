#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...enum.anim import Anim


class Context(View):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='Context', *args, **kwargs)
        self.visible = False

        self.__obj = None
        self.__anim = None
        self.__close_conn = None

        self.__transition_type = 'yScale'

    def open(self) -> None:
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
        self.visible = True

        if not self.__anim:
            self.__anim = QtCore.QPropertyAnimation(self.__obj, b'yScale')
            self.__anim.setDuration(100)

        self.__anim.setStartValue(0.0)
        self.__anim.setEndValue(1.0)
        self.__anim.start()

    def close(self) -> None:
        if not self.__obj:
            self.__obj = self._QtObject__obj.findChild(
                QtCore.QObject, 'scaleTransform')
        
        # Animation running
        if (self.__anim
                and self.__anim.state() == QtCore.QAbstractAnimation.Running):
            self.__anim.stop()

        # Animation
        if not self.__anim:
            self.__anim = QtCore.QPropertyAnimation(self.__obj, b'yScale')
            self.__anim.setDuration(100)

        self.__anim.setStartValue(1.0)
        self.__anim.setEndValue(0.0)
        self.__anim.setEasingCurve(QtCore.QEasingCurve.InCubic)
        
        self.__close_conn = self.__anim.finished.connect(self.__close)
        self.__anim.start()

    def __close(self) -> None:
        self.visible = False

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'
