#/usr/bin/env python3
import sys
import pathlib

from PySide6 import QtCore, QtGui, QtQml, QtQuick

from .handler import Handler
from .tools import change_element_style_state
from ..ui.layout import Layout
from ..ui.main_frame import MainFrame
from ..ui.element import Element

class AppEventFilter(QtCore.QObject):
    """..."""
    def __init__(self, main_rect: QtQuick.QQuickItem, style: dict) -> None:
        """..."""
        super().__init__()
        self.__main_rect = main_rect
        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)
        self.__style = style

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """..."""
        if event.type() == QtCore.QEvent.WindowActivate:
            self.__main_rect.setProperty('isActive', 'true')
            self.__state_style()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            self.__main_rect.setProperty('isActive', 'false')
            self.__state_style(':inactive')
        
        return super().eventFilter(obj, event)

    def __state_style(self, state: str = '') -> None:
        # MainFrame state colors
        self.__main_rect.setProperty(
            'color',
            self.__style[f'[MainFrame{state}]']['background_color'])
        self.__main_rect.setProperty(
            'borderColor',
            self.__style[f'[MainFrame{state}]']['border_color'])

        for element in self.__childrens:  # element.metaObject().className()
            change_element_style_state(element, state, self.__style)


class Application(object):
    """..."""
    def __init__(
            self, main_frame: MainFrame = MainFrame
            # handler: Handler = Handler
            ) -> None:
        """..."""
        self.__ui = main_frame()
        self.__path = pathlib.Path(__file__).parent.parent

        self.__qml_code = None
        self.__qml_code_iterator = 0
        self.__qml_path = self.__path /'static'/'qml'/'main.qml'
        self.__write_qml(self.__ui)

        self.__qt_gui_application = QtGui.QGuiApplication(sys.argv)
        self.__engine = QtQml.QQmlApplicationEngine()
        self.__engine.load(self.__qml_path)
        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__gui = self.__engine.rootObjects()[0]
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')

        # self.__handler = handler(self.__gui, self.__ui)
        self.__handler = Handler(self.__gui, self.__ui)

    def main_frame(self) -> Handler:
        """..."""
        return self.__ui

    def exec(self) -> None:
        """..."""
        event_filter = AppEventFilter(self.__main_rect, self.__ui.style)
        self.__gui.installEventFilter(event_filter)

        self.__engine.rootContext().setContextProperty('logic', self.__handler)
        sys.exit(self.__qt_gui_application.exec())

    def __write_qml(self, layout) -> None:
        # object_id as variable name
        for attr, value in layout.__dict__.items():
            if not attr.startswith('_'):
                gui_attr = getattr(layout, attr)
                if isinstance(gui_attr, Element):
                    # getattr(layout, attr).object_id = attr
                    gui_attr.object_id = attr

        # Parse QML
        end = '\n// **closing_key**'
        layout.qml, ui_close = layout.qml.split(end)
        for element in layout.added_objects:
            tab = ' ' * 12 if self.__qml_code_iterator == 0 else '    '

            element_close = None
            if end in element.qml:
                element_close = element.qml.split(end)[1]

            if isinstance(element, Layout):
                self.__qml_code_iterator += 1
                self.__write_qml(element)

            layout.qml += '\n'.join(
                [tab + x if x else ''
                for x in element.qml.split(end)[0].split('\n')])

            if element_close:
                layout.qml += element_close.replace('\n', '\n' + tab)

        self.__qml_code = layout.qml + ui_close
        self.__qml_path.write_text(self.__qml_code)
