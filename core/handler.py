#!/usr/bin/env python3
from PySide6 import QtCore, QtQuick

from ..ui import UI
from ..enum.shape import Shape


class Handler(QtCore.QObject):
    """Handles QML QtObject integration with UI graphical elements.

    Retrieves the graphic elements from the UI and integrates them with the 
    initial QtObject elements, and then sets the style of the elements and the 
    UI in each shape state.
    """
    def __init__(
            self, ui = UI, gui: QtQuick.QQuickWindow = None) -> None:
        """The init receives a QML-based QtObject and the app's UI.

        :param gui: The graphic Qml-Window instance (QQuickWindow).
        :param ui: The main UI app instance.
        """
        super().__init__()
        self.__ui = ui
        self.__gui = gui

        self.__elements = self.__gui.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

        self.__shape_border = None
        self.__gui.windowStateChanged.connect(self.__shape_changed)

        self.__signals = {
            '_clicked_signal': 'clicked', '_pressed_signal': 'pressed',
            '_released_signal': 'released', '_hovered_signal':'hoveredChanged',
            '_toggled_signal': 'toggled', '_checked_signal': 'checkedChanged',
            '_down_signal': 'downChanged', '_canceled_signal': 'canceled',
            '_active_signal': 'activeFocusChanged',
            '_enabled_signal': 'enabledChanged',
            '_visible_signal': 'visibleChanged'}
        self.__integrate_graphic_elements(self.__ui)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(ui={self.__ui!r}, gui={self.__gui!r})')

    def __str__(self) -> str:
        return self.__class__.__name__ + '()'

    @QtCore.Slot()
    def __integrate_graphic_elements(self, layout) -> None:
        # Integrate/Connect real Qt element on UI class element.
        # ui_ prefix is UI class element and gui_ is the Qt engine element.
        # >>> ui_element._QtObject__obj = gui_element
        
        for ui_element in layout._QtObject__items:

            qml_base = f'_{ui_element.__class__.__name__}__qml_base'  # Header
            if (ui_element._base == 'Layout' or
                    ui_element._base == 'Frame' or
                    hasattr(ui_element, qml_base) and
                    getattr(ui_element, qml_base) == 'Layout'):
                self.__integrate_graphic_elements(ui_element)

            if isinstance(ui_element, UI):
                gui_element = self.__gui.findChild(
                    QtCore.QObject, ui_element._QtObject__property('id'))
                
                if not gui_element:
                    continue

                ui_element._QtObject__obj = gui_element
                if ui_element._base == 'View': ui_element._render_signal.emit()
                for ui_signal, gui_signal in self.__signals.items():
                    if not hasattr(ui_element, ui_signal):
                        continue

                    call = getattr(ui_element, ui_signal).callback()
                    if callable(call) and hasattr(gui_element, gui_signal):
                        getattr(gui_element, gui_signal).connect(call)

    @QtCore.Slot()
    def __shape_changed(self, shape: QtCore.Qt.WindowState) -> None:
        if not self.__shape_border:
            self.__shape_border = (
                self.__gui.property('radiusTopLeft'),
                self.__gui.property('radiusTopRight'),
                self.__gui.property('radiusBottomRight'),
                self.__gui.property('radiusBottomLeft'),
                self.__gui.property('borderColor'),
                self.__gui.property('outLineColor'),
                self.__gui.property('backgroundColor'))

        if (shape == QtCore.Qt.WindowState.WindowFullScreen
                or shape == QtCore.Qt.WindowState.WindowMaximized):
            self.__gui.setProperty('radiusTopLeft', 0)
            self.__gui.setProperty('radiusTopRight', 0)
            self.__gui.setProperty('radiusBottomRight', 0)
            self.__gui.setProperty('radiusBottomLeft', 0)
            self.__gui.setProperty('borderColor', self.__shape_border[6])
            self.__gui.setProperty('outLineColor', self.__shape_border[6])
            self.__gui.setProperty('borderSpacing', 0)
        else:  # borderWidth outLineWidth
            self.__gui.setProperty('borderSpacing', 1)
            self.__gui.setProperty('radiusTopLeft', self.__shape_border[0])
            self.__gui.setProperty('radiusTopRight', self.__shape_border[1])
            self.__gui.setProperty('radiusBottomRight', self.__shape_border[2])
            self.__gui.setProperty('radiusBottomLeft', self.__shape_border[3])
            self.__gui.setProperty('borderColor', self.__shape_border[4])
            self.__gui.setProperty('outLineColor', self.__shape_border[5])

        if shape == QtCore.Qt.WindowState.WindowFullScreen:
            self.__ui._MainFrame__shape = Shape.FULL
        elif shape == QtCore.Qt.WindowState.WindowMaximized:
            self.__ui._MainFrame__shape = Shape.MAX
        else:
            self.__ui._MainFrame__shape = Shape.FRAME
        
        self.__gui.findChild(QtCore.QObject, 'canvas').requestPaint()

    @QtCore.Slot()
    def connections(self):
        """Processes callback properties for QML.
        """
        """
        Qt.LeftButton
        Qt.RightButton
        Qt.MiddleButton – scroll
        Qt.BackButton – botão "Voltar" do mouse
        Qt.ForwardButton – botão "Avançar" do mouse
        Qt.TaskButton – botão adicional (geralmente botão de aplicativo)
        Qt.ExtraButton1 at Qt.ExtraButton24 – Extras (para mouses avançados)
        Qt.AllButtons

        Left and right click:
            acceptedButtons: Qt.LeftButton | Qt.RightButton

        Any buttons:
            acceptedButtons: Qt.AllButtons

        Only middle:
            acceptedButtons: Qt.MiddleButton
        """
        self.__ui._right_pressed_signal.emit()

    @QtCore.Slot()
    def start_move(self) -> None:
        """Move the apps UI natively in CSD mode.

        Qt internal method to use native system movement when dragging/moving 
        the application UI.
        """
        self.__gui.startSystemMove()

    @QtCore.Slot(int)
    def start_resize(self, edge: int) -> None:
        """Resize the app UI natively in CSD mode.

        Qt's built-in method to use native system resizing in the apps UI.
        """
        edge = QtCore.Qt.Edge(edge)
        self.__gui.startSystemResize(edge)

    @QtCore.Slot()
    def max_min(self) -> None:
        QtCore.QTimer.singleShot(100, self.__max_min)

    @QtCore.Slot()
    def __max_min(self) -> None:
        if self.__gui.windowState() == QtCore.Qt.WindowState.WindowMaximized:
            self.__gui.showNormal()
        else:
            self.__gui.showMaximized()
