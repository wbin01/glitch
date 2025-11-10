#!/usr/bin/env python3
from PySide6 import QtCore

from .view import View
from ...core.signal import Signal


class MaxButton(View):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='MaxButton', *args, **kwargs)
        self.__mouse_press_signal = Signal()
        self.__max, self.__restore = None, None
        self.__hover, self.__restore_hover = None, None
        self.__clicked, self.__restore_clicked = None, None

        self._app_signal.connect(self.__on_app_signal)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _mouse_press_signal(self) -> Signal:
        """..."""
        return self.__mouse_press_signal

    def __on_app_signal(self):
        self.__mouse_press_signal.connect(self.__max_restore)
        self._app._render_signal.connect(
            lambda: self._app._shape_signal.connect(self.__update_icon))

    def __max_restore(self) -> None:
        # showNormal() .showFullScreen()
        self.__saved_properties()
        shape = self._app._QtObject__obj.windowState()
        if shape == QtCore.Qt.WindowState.WindowMaximized:
            self._app._QtObject__obj.showNormal()
            self.__max_icon()
        else:
            self._app._QtObject__obj.showMaximized()
            self.__restore_icon()

    def __update_icon(self) -> None:
        self.__saved_properties()
        shape = self._app._QtObject__obj.windowState()
        if (shape == QtCore.Qt.WindowState.WindowMaximized or
                shape == QtCore.Qt.WindowState.WindowFullScreen):
            self.__restore_icon()
        else:
            self.__max_icon()

    def __max_icon(self) -> None:
        self._QtObject__set_property('normalIcon', self.__max)
        self._QtObject__set_property('hoverIcon', self.__hover)
        self._QtObject__set_property('clickedIcon', self.__clicked)

    def __restore_icon(self) -> None:
        self._QtObject__set_property('normalIcon', self.__restore)
        self._QtObject__set_property('hoverIcon', self.__restore_hover)
        self._QtObject__set_property('clickedIcon', self.__restore_clicked)

    def __saved_properties(self) -> None:
        if not self.__max:
            self.__max = self._QtObject__property('normalIcon')
            self.__restore = self._QtObject__property('restoreNormalIcon')

            self.__hover = self._QtObject__property('hoverIcon')
            self.__restore_hover = self._QtObject__property('restoreHoverIcon')

            self.__clicked = self._QtObject__property('clickedIcon')
            self.__restore_clicked = self._QtObject__property(
                'restoreClickedIcon')
