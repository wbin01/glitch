#!/usr/bin/env python3
import sys
import pathlib

from PySide6 import QtCore, QtGui, QtQml, QtQuick

from .handler import Handler
from .application_style import change_element_style_state, style_value
from ..ui.base import Element, Layout
from ..ui.layout import Frame


class AppEventFilter(QtCore.QObject):
    """Application event filter.

    Filters the Frame state and adapts the elements.
    """
    def __init__(
            self, ui: Frame, gui: QtQuick.QQuickWindow, style: dict) -> None:
        """
        :param ui: The main Frame app instance.
        :param gui: The graphic Qml-Window instance (QQuickWindow).
        :param style: The application styles dict.
        """
        super().__init__()
        self.__ui = ui
        self.__gui = gui.findChild(QtCore.QObject, 'mainRect')
        self.__style = style
        self.__elements = self.__gui.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)
    
    @QtCore.Slot()
    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Adapts the style of the elements.

        Filters the active state of the Frame and changes the style of all 
        elements accordingly.

        :param obj: QtCore.QObject.
        :param event: QtCore.QEvent.
        """
        if event.type() == QtCore.QEvent.WindowActivate:
            self.__gui.setProperty('isActive', 'true')
            self.__state_style()
        elif event.type() == QtCore.QEvent.WindowDeactivate:
            self.__gui.setProperty('isActive', 'false')
            self.__state_style(':inactive')
        
        return super().eventFilter(obj, event)

    @QtCore.Slot()
    def __state_style(self, state: str = '') -> None:
        # MainFrame state colors
        frame = f'[{self.__ui._name}{state}]'
        self.__gui.setProperty(
            'backgroundColor',
            style_value(self.__style, frame, 'background_color'))
        self.__gui.setProperty(
            'borderColor', style_value(self.__style, frame, 'border_color'))
        self.__gui.findChild(QtCore.QObject, 'canvas').requestPaint()

        for element in self.__elements:  # element.metaObject().className()
            change_element_style_state(element, state, self.__style)

    def __str__(self) -> str:
        return "<class 'AppEventFilter'>"


class Application(object):
    """Manages the application.

    Handles the processes necessary for the application to function properly.
    """
    def __init__(self, frame: Frame = Frame) -> None:
        """
        :param frame: The Application Frame.
        """
        self.__ui = frame()
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
        self.__handler = Handler(self.__gui, self.__ui)

    def frame(self) -> Frame:
        """The Application Frame.
        
        The Frame class passed to the constructor of this class.
        """
        return self.__ui

    def exec(self) -> None:
        """Run the application.

        Manages the processes to start the Application Frame and execute it.
        """
        event_filter = AppEventFilter(self.__ui, self.__gui, self.__ui.style)
        self.__gui.installEventFilter(event_filter)
        self.__engine.rootContext().setContextProperty('logic', self.__handler)
        sys.exit(self.__qt_gui_application.exec())

    def __write_qml(self, layout) -> None:
        # object_id as variable name
        for attr, value in layout.__dict__.items():
            if not attr.startswith('_'):
                element = getattr(layout, attr)
                if isinstance(element, Element):
                    element._id = attr

        # TODO: update style

        # Parse QML
        end = '\n// Close'
        layout._qml, ui_close = layout._qml.split(end)
        for element in layout.items():
            tab = ' ' * 12 if self.__qml_code_iterator == 0 else '    '

            element_close = None
            if end in element._qml:
                element_close = element._qml.split(end)[1]

            if isinstance(element, Layout):
                self.__qml_code_iterator += 1
                self.__write_qml(element)

            layout._qml += '\n'.join(
                [tab + x if x else ''
                for x in element._qml.split(end)[0].split('\n')])

            if element_close:
                layout._qml += element_close.replace('\n', '\n' + tab)

        self.__qml_code = layout._qml + ui_close
        self.__qml_path.write_text(self.__qml_code)

    def __str__(self) -> str:
        return "<class 'Application'>"
