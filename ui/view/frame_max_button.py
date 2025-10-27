#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...core.signal import Signal


class FrameMaxButton(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='FrameMaxButton', *args, **kwargs)
        self.__mouse_press_signal = Signal()

        self._frame_signal.connect(
            lambda: self.__mouse_press_signal.connect(self.__state_action))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _mouse_press_signal(self) -> Signal:
        """..."""
        return self.__mouse_press_signal

    def __state_action(self):
        state = self._frame._QtObject__obj.window().windowState()
        if state == QtCore.Qt.WindowState.WindowMaximized:
            self._frame._QtObject__obj.window().showNormal()
        else:
            self._frame._QtObject__obj.window().showMaximized()
        """
        .showNormal()
        .showMaximized()
        .showMinimized()
        .showFullScreen()
        """
