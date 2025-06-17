#/usr/bin/env python3
from .element import Element


class Label(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__text = self._obj.property('text')

    @property
    def text(self) -> str:
        """..."""
        return self._obj.property('text')

    @text.setter
    def text(self, text: str) -> None:
        self._obj.setProperty('text', text)

    # def connect(self, func: callable) -> None:
    #     self._obj.clicked.connect(func)
