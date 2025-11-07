#!/usr/bin/env python3
from ..ui import UI


qml_imports = """
import QtQuick
import QtQuick.Controls
import QtQuick.Controls.AdaptiveGlitch
import QtQuick.Layouts
import QtQuick.Shapes
"""

class QmlBuilder(object):
    """..."""
    def __init__(self, ui: UI) -> None:
        """
        :param ui:
        """
        self.__ui = ui
        self.__qml_code = ''
        self.__first_iteration = True
        self.__suffix = 0
        self.__write_qml(self.__ui)
        self.__qml_finish()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(ui={self.__ui!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(ui={self.__ui!r})'

    @property
    def _qml(self) -> str:
        """..."""
        return self.__qml_code

    def __write_qml(self, ui: UI, tab: str = '') -> None:
        if not hasattr(ui, '_QtObject__items'):
            return
        self.__suffix += 1

        # Layout ID
        if '<id>' in ui.qml and self.__first_iteration:
            id_ = f'{ui.__class__.__name__.lower()}_{self.__suffix}'
            ui.qml = ui.qml.replace('<id>', f'{id_}').replace(
                '// Close ' + ui._name, '// Close ' + id_)

        # Childs ID
        for name, value in ui.__dict__.items():
            element = getattr(ui, name)
            if isinstance(element, UI):
                id_ = f'{name.lower()}_{self.__suffix}'
                element.qml = element.qml.replace('<id>', f'{id_}').replace(
                    '// Close ' + element._name, '// Close ' + id_)

        # Headers and his properties
        header, body = ui.qml.split('// +')
        qml_end = body.strip('\n')

        for line in header.split('\n'):
            if '//' not in line:
                self.__qml_code += tab + line + '\n'
        self.__qml_code = self.__qml_code.strip() + '\n'

        # Sub Childs
        tab += '    '
        self.__first_iteration = False
        for element in ui._QtObject__items:
            element_items = (getattr(element, '_QtObject__items')
                if hasattr(element, '_QtObject__items') else None)
            
            if element_items and isinstance(element_items, list):
                self.__write_qml(element, tab)
            else:
                for qml_line in element.qml.split('\n'):
                    if '// Close' in qml_line:
                        qml_line = qml_line.split('// Close')[0].rstrip()
                    if qml_line and '//' not in qml_line:
                        self.__qml_code += tab + qml_line + '\n'
        # Close
        self.__qml_code = self.__qml_code + tab[:-4] + qml_end + '\n'

    def __qml_finish(self) -> None:
        sparse_qml = ''
        for line in self.__qml_code.split('\n'):
            if line.strip():
                if '{' in line:
                    sparse_qml += '\n' + line + '\n'
                elif '}' in line:
                    sparse_qml += line + '\n'
                else:
                    sparse_qml += line + '\n'
        self.__qml_code = qml_imports.lstrip() + '\n' + sparse_qml.replace(
            '// Close ', '// ')
