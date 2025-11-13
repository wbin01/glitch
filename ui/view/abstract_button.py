#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class AbstractButton(View):
    def __init__(
            self, name='Button', icon_source: str = None, *args, **kwargs
            ) -> None:
        super().__init__(name=name, icon_source=icon_source, *args, **kwargs)
        self.__icon = icon_source
        if self.__icon:
            self._QtObject__set_property('icon.source', self.__icon)

        # Signals
        self.__checked_signal = Signal()
        self.__clicked_signal = Signal()
        self.__hovered_signal = Signal()
        self.__pressed_signal = Signal()
        self.__released_signal = Signal()
        self.__toggled_signal = Signal()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}()'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}()'

    @property
    def checkable(self) -> bool:
        """..."""
        value = self._QtObject__property('checkable')
        if value is None:
            return False
        return value

    @checkable.setter
    def checkable(self, value: str) -> None:
        self._QtObject__set_property('checkable', value)

    @property
    def checked(self) -> bool:
        """..."""
        value = self._QtObject__property('checked')
        if value is None:
            return False
        return value

    @checked.setter
    def checked(self, value: str) -> None:
        self._QtObject__set_property('checked', value)

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
