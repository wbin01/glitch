#!/usr/bin/env python3
from .view import View


class Label(View):
    def __init__(self, text: str = None, *args, **kwargs) -> None:
        super().__init__(name='Label', *args, **kwargs)
        self.__text = text
        if self.__text:
            self._QtObject__set_property('text', self.__text)

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
