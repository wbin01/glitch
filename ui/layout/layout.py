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

        self.__aligns = {
            Align.BASE_LINE: 'Qt.AlignBaseline',
            Align.BOTTOM: 'Qt.AlignBottom',
            Align.BOTTOM_LEFT: 'Qt.AlignBottom | Qt.AlignLeft',
            Align.BOTTOM_RIGHT: 'Qt.AlignBottom | Qt.AlignRight',
            Align.CENTER: 'Qt.AlignCenter',
            Align.H_CENTER: 'Qt.AlignHCenter',
            Align.JUSTIFY: 'Qt.AlignJustify',
            Align.LEFT: 'Qt.AlignLeft',
            Align.RIGHT: 'Qt.AlignRight',
            Align.TOP: 'Qt.AlignTop',
            Align.TOP_LEFT: 'Qt.AlignTop | QtCore.Qt.AlignLeft',
            Align.TOP_RIGHT: 'Qt.AlignTop | QtCore.Qt.AlignRight',
            Align.V_CENTER: 'Qt.AlignVCenter',
            Align.NONE: '0'}

        self._QtObject__set_property('Layout.alignment', 'alignment')
        self._QtObject__set_property('property int alignment', 'Qt.AlignTop')
        
        self._QtObject__set_property('Layout.fillWidth', 'fillWidth')
        self._QtObject__set_property('property bool fillWidth', 'true')
        
        self._QtObject__set_property('Layout.fillHeight', 'fillHeight')
        self._QtObject__set_property('property bool fillHeight', 'false')

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def align(self) -> tuple:
        """..."""
        if not self._QtObject__obj:
            return Align.TOP, True, False

        fill_width = self._QtObject__property('fillWidth')
        fill_height = self._QtObject__property('fillHeight')
        alignment = self._QtObject__property('alignment')

        for align in self.__aligns.keys():
            if align.value == alignment:
                return align, fill_width, fill_height

    @align.setter
    def align(self, align: Align | tuple) -> None:
        if isinstance(align, Align):
            if not self._QtObject__obj:
                self._QtObject__set_property('alignment', self.__aligns[align])
            else:
                self._QtObject__set_property('alignment', align.value)
            return

        if not align:
            return

        fill_width = None
        fill_height = None
        len_align = len(align)
        
        if len_align == 1:
            align = align[0]
        elif len_align == 2:
            align, fill_width = align
        else:
            align, fill_width, fill_height = align[:3]
        
        if fill_width is not None:
            self._QtObject__set_property('fillWidth', fill_width)

        if fill_height is not None:
            self._QtObject__set_property('fillHeight', fill_height)

        if align is not None:
            if not self._QtObject__obj:
                self._QtObject__set_property('alignment', self.__aligns[align])
            else:
                self._QtObject__set_property('alignment', align.value)

    @property
    def _base(self):
        """..."""
        return self.__base
