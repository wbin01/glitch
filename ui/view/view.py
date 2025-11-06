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
        visible = self._QtObject__property('visible')
        if visible is None:
            return True
        return visible

    @visible.setter
    def visible(self, visible: bool) -> None:
        self._QtObject__set_property('visible', visible)
