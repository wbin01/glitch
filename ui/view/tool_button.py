#!/usr/bin/env python3
import pathlib

from .view import View
from ...core.signal import Signal


class ToolButton(View):
    def __init__(self, icon_source: str = None, *args, **kwargs) -> None:
        super().__init__(name='ToolButton', *args, **kwargs)
        self.__checked_signal = Signal()
        self.__clicked_signal = Signal()
        self.__hovered_signal = Signal()
        self.__pressed_signal = Signal()
        self.__released_signal = Signal()
        self.__toggled_signal = Signal()

        self.__icon = icon_source if icon_source else pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'empty.svg'
        if self.__icon:
            self._QtObject__set_property('icon.source', self.__icon)
        # self._QtObject__set_property('checkable', 'true')
        # self._QtObject__set_property(
        #     'onToggled', 'console.log("Estado:", checked)')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def _checked_signal(self) -> Signal:
        """..."""
        return self.__checked_signal

    @property
    def _clicked_signal(self) -> Signal:
        """..."""
        return self.__clicked_signal

    @property
    def _hovered_signal(self) -> Signal:
        """..."""
        return self.__hovered_signal

    @property
    def _pressed_signal(self) -> Signal:
        """..."""
        return self.__pressed_signal

    @property
    def _released_signal(self) -> Signal:
        """..."""
        return self.__released_signal

    @property
    def _toggled_signal(self) -> Signal:
        """..."""
        return self.__toggled_signal
