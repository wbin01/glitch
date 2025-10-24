#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add


class Layout(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # TODO: Create this properties
        self._QtObject__set_property('spacing', 6)
        self._QtObject__set_property('clip', 'true')
        self._QtObject__set_property('Layout.alignment', 'Qt.AlignTop')
        self._QtObject__set_property('Layout.fill_width', 'false')
        self._QtObject__set_property('Layout.left_margin', 15)

    def __repr__(self) -> str:
        return self.__class__.__name__
