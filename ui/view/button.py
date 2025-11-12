#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class Button(View):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='Button', *args, **kwargs)
        self.__checked_signal = Signal()
        self.__clicked_signal = Signal()
        self.__hovered_signal = Signal()
        self.__pressed_signal = Signal()
        self.__released_signal = Signal()
        self.__toggled_signal = Signal()

        self.__text = text
        if self.__text:
            self._QtObject__set_property('text', self.__text)

        self._QtObject__set_property('Layout.fillWidth', 'true')
        # self._QtObject__set_property('checkable', 'true')
        # self._QtObject__set_property(
        #     'onToggled', 'console.log("Estado:", checked)')
        # TODO
        # self._QtObject__set_property(
        #     'icon.source',
        #     '/usr/share/icons/breeze-dark/actions/16/document-open.svg')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(text={self.__text!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__text!r})'

    @property
    def text(self) -> str:
        """..."""
        return self._QtObject__property('text')

    @text.setter
    def text(self, text: str) -> None:
        self.__text = text
        self._QtObject__set_property('text', text)

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
