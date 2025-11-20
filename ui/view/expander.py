#!/usr/bin/env python3
from .view import View


class Expander(View):
    def __init__(
            self, vertical: bool = None, horizontal: bool = None,
            *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__vertical = vertical
        self.__horizontal = horizontal

        if self.__vertical and not self.__horizontal:
            self._QtObject__set_property('Layout.fillHeight', True)
            self._QtObject__set_property('Layout.fillWidth', False)
        
        elif not self.__vertical and self.__horizontal:
            self._QtObject__set_property('Layout.fillHeight', False)
            self._QtObject__set_property('Layout.fillWidth', True)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}('
            f'vertical={self.__vertical!r}, horizontal={self.__horizontal!r})')

    def __str__(self) -> str:
        return (f'{self.__class__.__name__}()')
