#!/usr/bin/env python3
from ..ui import UI
from ..mixin import Add
from ...enum.align import Align


class Layout(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__base = 'Layout'
        self._QtObject__set_property('clip', 'true')

        self._QtObject__set_property('Layout.alignment', 'Qt.AlignTop')
        self._QtObject__set_property(
            'property int alignment', 'Layout.alignment')
        self.__aligns = [
            Align.BASE_LINE, Align.BOTTOM, Align.BOTTOM_LEFT,
            Align.BOTTOM_RIGHT, Align.CENTER, Align.H_CENTER,
            Align.JUSTIFY, Align.LEFT, Align.RIGHT, Align.TOP, Align.TOP_LEFT,
            Align.TOP_RIGHT, Align.V_CENTER]

        self._QtObject__set_property('Layout.fillWidth', 'true')

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def align(self) -> Align:
        """..."""
        alignment = self._QtObject__property('alignment')
        for align in self.__aligns:
            if align.value == alignment:
                return align

    @align.setter
    def align(self, align: Align) -> None:
        self._QtObject__set_property('alignment', align.value)

    @property
    def _base(self):
        """..."""
        return self.__base
