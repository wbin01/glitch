#!/usr/bin/env python3
from PySide6 import QtCore, QtQuick
from ..ui import UI


class Handler(QtCore.QObject):
    """Handles QML QtObject integration with UI graphical elements.

    Retrieves the graphic elements from the UI and integrates them with the 
    initial QtObject elements, and then sets the style of the elements and the 
    UI in each state.
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

        self.__state_border = None
        self.__gui.windowStateChanged.connect(self.__state_changed)
        self.__integrate_graphic_elements(self.__ui)

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(ui={self.__ui!r}, gui={self.__gui!r})')

    def __str__(self) -> str:
        return self.__class__.__name__ + '()'

    @QtCore.Slot()
    def __integrate_graphic_elements(self, layout) -> None:
        # Integration UI graphic elements into the Main UI QtObject.
        signals = ['_mouse_press_signal', '_state_signal']
        for element in layout._QtObject__items:

            qml_base = f'_{element.__class__.__name__}__qml_base'
            if (element._base == 'Layout' or
                    hasattr(element, qml_base) and
                    getattr(element, qml_base) == 'Layout'):
                self.__integrate_graphic_elements(element)

            if isinstance(element, UI):
                obj_value = self.__gui.findChild(
                    QtCore.QObject, element._QtObject__property('id'))
                
                if not obj_value:
                    continue

                element._QtObject__obj = obj_value
                for signal in signals:
                    if not hasattr(element, signal):
                        continue

                    call = getattr(element, signal).callback()
                    if callable(call):
                        element._QtObject__obj.released.connect(call)

    @QtCore.Slot()
    def __state_changed(self, state: QtCore.Qt.WindowState) -> None:
        if not self.__state_border:
            self.__state_border = (
                self.__gui.property('radiusTopLeft'),
                self.__gui.property('radiusTopRight'),
                self.__gui.property('radiusBottomRight'),
                self.__gui.property('radiusBottomLeft'),
                self.__gui.property('borderColor'),
                self.__gui.property('outLineColor'),
                self.__gui.property('backgroundColor'))

        if (state == QtCore.Qt.WindowState.WindowFullScreen
                or state == QtCore.Qt.WindowState.WindowMaximized):
            self.__gui.setProperty('radiusTopLeft', 0)
            self.__gui.setProperty('radiusTopRight', 0)
            self.__gui.setProperty('radiusBottomRight', 0)
            self.__gui.setProperty('radiusBottomLeft', 0)
            self.__gui.setProperty('borderColor', self.__state_border[6])
            self.__gui.setProperty('outLineColor', self.__state_border[6])
            self.__gui.setProperty('color', self.__state_border[6])
        else:  # borderWidth outLineWidth
            self.__gui.setProperty('radiusTopLeft', self.__state_border[0])
            self.__gui.setProperty('radiusTopRight', self.__state_border[1])
            self.__gui.setProperty('radiusBottomRight', self.__state_border[2])
            self.__gui.setProperty('radiusBottomLeft', self.__state_border[3])
            self.__gui.setProperty('borderColor', self.__state_border[4])
            self.__gui.setProperty('outLineColor', self.__state_border[5])
            self.__gui.setProperty('color', 'transparent')

        self.__gui.findChild(QtCore.QObject, 'canvas').requestPaint()

    @QtCore.Slot()
    def connections(self):
        """Processes callback properties for QML.
        
        MOUSE_RIGHT_PRESS Event
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
        print('Right clicked')
        # self.__ui.mouse_right_press_signal.callback()()

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
