#!/usr/bin/env python3
from PySide6.QtQml import QQmlComponent, QQmlEngine, QQmlContext
from PySide6.QtCore import QUrl

from ..ui import UI
from ..mixin import Add
from ...enum.align import Align


binding = """
    Binding {
        target: <id>.Layout
        property: "alignment"
        value: <id>.layoutAlignment
    }
    Binding {
        target: <id>.Layout
        property: "fillWidth"
        value: <id>.layoutFillWidth
    }
    Binding {
        target: <id>.Layout
        property: "fillHeight"
        value: <id>.layoutFillHeight
    }
    // +
"""

class AbstractLayout(Add, UI):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, base='Layout', **kwargs)
        self._QtObject__set_property('clip', 'true')
        self.__align_has_set = False
        self.__alignment = Align.TOP
        self.__fill_width = True
        self.__fill_height = True

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

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def align(self) -> tuple:
        """..."""
        return self.__alignment, self.__fill_width, self.__fill_height

    @align.setter
    def align(self, align: Align | tuple) -> None:
        if not align: return

        if not self.__align_has_set:
            self._QtObject__set_property('property bool fillWidth', 'true')
            self._QtObject__set_property('property bool fillHeight', 'true')
            self._QtObject__set_property(
                'property int alignment', 'Qt.AlignTop')
            
            self._QtObject__set_property('Layout.alignment', 'alignment')
            self._QtObject__set_property('Layout.fillWidth', 'fillWidth')
            self._QtObject__set_property('Layout.fillHeight', 'fillHeight')

            self._QtObject__qml = self._QtObject__qml.replace('// +', binding)
            self.__align_has_set = True

        if isinstance(align, Align):
            if not self._QtObject__obj:
                self._QtObject__set_property('alignment', self.__aligns[align])
            else:
                self._QtObject__set_property('alignment', align.value)
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
            if not self._QtObject__obj:
                self._QtObject__set_property('fillWidth', fill_width)
            else:
                self.__binding(self._QtObject__obj, 'fillWidth', fill_width)
            self.__fill_width = fill_width

        if fill_height is not None:
            if not self._QtObject__obj:
                self._QtObject__set_property('fillHeight', fill_height)
            else:
                self.__binding(self._QtObject__obj, 'fillHeight', fill_height)
            self.__fill_height = fill_height

        if align is not None:
            if not self._QtObject__obj:
                self._QtObject__set_property('alignment', self.__aligns[align])
            else:
                self.__binding(
                    self._QtObject__obj, 'alignment', int(align.value))
            self.__alignment = align

    def __binding(self, item, layout_prop, value):
        engine = QQmlEngine.contextForObject(item).engine()
        qml_code = f"""
            import QtQuick
            import QtQuick.Layouts

            Binding {{
                target: layoutTarget.Layout
                property: "{layout_prop}"
                value: bindingValue
            }}
        """

        component = QQmlComponent(engine)
        component.setData(qml_code.encode('utf-8'), QUrl())

        context = QQmlContext(engine.rootContext())
        context.setContextProperty('layoutTarget', item)
        context.setContextProperty('bindingValue', value)

        binding_ = component.create(context)
        binding_.setParent(item)
