#!/usr/bin/env python3
import pathlib

from .view import View


class Image(View):
    def __init__(self, image: str = None, *args, **kwargs) -> None:
        super().__init__(name='Image', *args, **kwargs)

        self.__image = image if image else pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'glitch.svg'

        self._QtObject__set_property('source', self.__image)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(image={self.__image!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__image!r})'
