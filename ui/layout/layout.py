#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Layout(UI, Add):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__base = 'Layout'
        # TODO: Create this properties
        self._QtObject__set_property('clip', 'true')
        self._QtObject__set_property('Layout.alignment', 'Qt.AlignTop')
        self._QtObject__set_property('Layout.fillWidth', 'true')
        # self._QtObject__set_property('Layout.leftMargin', 15)

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def _base(self):
        """..."""
        return self.__base
