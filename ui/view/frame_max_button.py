#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...core.signal import Signal


class FrameMaxButton(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='FrameMaxButton', *args, **kwargs)
        self.__mouse_press_signal = Signal()
        self.__max, self.__restore = None, None
        self.__hover, self.__restore_hover = None, None
        self.__clicked, self.__restore_clicked = None, None

        self._frame_signal.connect(
            lambda: self.__mouse_press_signal.connect(self.__max_restore))

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _mouse_press_signal(self) -> Signal:
        """..."""
        return self.__mouse_press_signal

    def __max_restore(self) -> None:
        """
        .showNormal()
        .showMaximized()
        .showMinimized()
        .showFullScreen()
        """
        if not self.__max:
            self.__max = self._QtObject__property('normalIcon')
            self.__restore = self._QtObject__property('restoreNormalIcon')

            self.__hover = self._QtObject__property('hoverIcon')
            self.__restore_hover = self._QtObject__property('restoreHoverIcon')

            self.__clicked = self._QtObject__property('clickedIcon')
            self.__restore_clicked = self._QtObject__property(
                'restoreClickedIcon')

        state = self._frame._QtObject__obj.window().windowState()
        if state == QtCore.Qt.WindowState.WindowMaximized:
            self._frame._QtObject__obj.window().showNormal()
            self._QtObject__set_property('normalIcon', self.__max)
            self._QtObject__set_property('hoverIcon', self.__hover)
            self._QtObject__set_property('clickedIcon', self.__clicked)
        else:
            self._frame._QtObject__obj.window().showMaximized()
            self._QtObject__set_property('normalIcon', self.__restore)
            self._QtObject__set_property('hoverIcon', self.__restore_hover)
            self._QtObject__set_property('clickedIcon', self.__restore_clicked)
