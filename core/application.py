#!/usr/bin/env python3
import sys
import pathlib

from PySide6 import QtCore, QtGui, QtQml, QtQuick

from .handler import Handler
from .qml_builder import QmlBuilder
from ..platform_ import Platform
from ..platform_.qml_style import QmlStyle
from ..ui import UI
from ..ui.frame.app_frame import AppFrame


class AppEventFilter(QtCore.QObject):
    """Application event filter.

    Filters the UI events and adapts the elements.
    """
    def __init__(self, ui: UI, gui: QtQuick.QQuickWindow) -> None:
        """
        :param ui: The main UI app instance.
        :param gui: The graphic Qml-Window instance (QQuickWindow).
        :param style: The application styles dict.
        """
        super().__init__()
        self.__ui = ui
        self.__gui = gui
        self.__paint = 0
        self.__elements = self.__gui.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(ui={self.__ui!r}, gui={self.__gui!r})')

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(ui={self.__ui!r})'
    
    @QtCore.Slot()
    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Adapts the style of the elements.

        Filters the active events of the UI and changes the style of all 
        elements accordingly.

        :param obj: QtCore.QObject.
        :param event: QtCore.QEvent.
        """
        event_type = event.type()

        if event_type == QtCore.QEvent.WindowActivate:
            self.__ui._active_signal.emit()
        
        elif event_type == QtCore.QEvent.WindowDeactivate:
            self.__ui._inactive_signal.emit()

        if event_type == QtCore.QEvent.Resize:
            self.__ui._resize_signal.emit()

        elif event_type == QtCore.QEvent.WindowStateChange:
            if hasattr(self.__ui, '_shape_signal'):
                self.__ui._shape_signal.emit()

        elif event_type == QtCore.QEvent.Paint:
            if not self.__paint:
                self.__ui._render_signal.emit()
                self.__paint = 1

        return super().eventFilter(obj, event)


class Application(object):
    """Manages the application.

    Handles the processes necessary for the application to function properly.
    """
    def __init__(self, frame: UI = UI, dev: bool = True) -> None:
        """
        :param frame: The Application UI.
        """
        self.__ui = frame()
        self.__dev = dev

        self.__path = pathlib.Path(__file__).parent.parent
        self.__qml_path = self.__path /'static'/'qml'/'main.qml'
        self.__qml_theme_path = self.__path / 'static' / 'qml'
        
        qml = QmlBuilder(self.__ui)
        if self.__dev:
            self.__qml_path.write_text(qml._qml)

        # Style
        self.__platform = Platform()
        qml_style = QmlStyle(self.__platform.style, self.__qml_theme_path)
        qml_style.build()
        self.__ui._Frame__platform = self.__platform
        self.__ui._platform_signal.emit()

        self.__qt_gui_application = QtGui.QGuiApplication(sys.argv)
        self.__engine = QtQml.QQmlApplicationEngine()
        self.__engine.addImportPath(str(self.__qml_theme_path))
        self.__engine.load(self.__qml_path)
        
        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__gui = self.__engine.rootObjects()[0]
        self.__ui._QtObject__obj = self.__gui
        self.__ui._Frame__engine = self.__engine
        self.__ui._Frame__qt_qml = QtQml
        self.__ui._Frame__qt_core = QtCore
        self.__handler = Handler(self.__ui, self.__gui)

        # Properties
        self.__name = None
        self.__icon = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def name(self) -> str:
        """..."""
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
        self.__ui._QtObject__set_property('title', name)
        if isinstance(self.__ui, AppFrame):
            if not self.__ui.header.text:
                self.__ui.header.text = name

    @property
    def _frame(self) -> UI:
        """The Application UI UI.
        
        The UI class passed to the constructor of this class.
        """
        return self.__ui

    def exec(self) -> None:
        """Run the application.

        Manages the processes to start the Application UI and execute it.
        """
        event_filter = AppEventFilter(self.__ui, self.__gui)
        self.__gui.installEventFilter(event_filter)
        self.__engine.rootContext().setContextProperty('logic', self.__handler)
        self.__qt_gui_application.exec()
