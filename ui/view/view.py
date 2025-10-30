#!/usr/bin/env python3
from ..ui import UI


class View(UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__base = 'View'

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def _base(self):
        """..."""
        return self.__base

    @property
    def visible(self) -> bool:
        """..."""
        return self._QtObject__property('visible')

    @visible.setter
    def visible(self, visible: bool) -> None:
        visible = 'true' if visible else 'false'
        self._QtObject__set_property('visible', visible)
