#!/usr/bin/env python3
from .view import View
from ...core.signal import Signal


class Button(View):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='Button', *args, **kwargs)
        self.mouse_press_signal = Signal()
        self.__text = text
        if self.__text:
            self._QtObject__set_property('text', self.__text)
        # TODO
        self._QtObject__set_property(
            'icon.source',
            '/usr/share/icons/breeze-dark/actions/16/document-open.svg')

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
