#/usr/bin/env python3
from .layout import Layout


class MainFrame(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.__style = None

    @property
    def style(self) -> dict:
        """..."""
        return self.__style

    @style.setter
    def style(self, style: dict) -> None:
        self.__style = style

    @property
    def height(self) -> int:
        """..."""
        return self._obj.property('_height')

    @height.setter
    def height(self, height: int) -> None:
        self._obj.setProperty('_height', height)
