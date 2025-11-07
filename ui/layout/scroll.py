#!/usr/bin/env python3
from .layout import Layout


class Scroll(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(name='ScrollView', *args, **kwargs)
        self._QtObject__set_property('Layout.fillWidth', 'true')
        self._QtObject__set_property('Layout.fillHeight', 'true')
        # self._QtObject__set_property('contentWidth', 'availableWidth')
        # self._QtObject__set_property('clip', 'true')

    def __repr__(self) -> str:
        return self.__class__.__name__
