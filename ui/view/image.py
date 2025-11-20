#!/usr/bin/env python3
import pathlib

from .view import View


class Image(View):
    def __init__(self, image: str = None, *args, **kwargs) -> None:
        super().__init__(name='Image', *args, **kwargs)

        if not image: self.__image = pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'image.svg'

        elif image == 'glitch': self.__image = pathlib.Path(
            __file__).parent.parent.parent / 'static' / 'icons' / 'glitch.svg'
        else:
            self.__image = pathlib.Path(image)
        
        if not self.__image.exists(): self.__image = pathlib.Path(
                __file__).parent.parent.parent /'static'/'icons'/'image.svg'

        self._QtObject__set_property('source', self.__image)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(image={self.__image!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.__image!r})'
