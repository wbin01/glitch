#!/usr/bin/env python3
from PySide6 import QtCore, QtQuick

from .application_shares import change_element_style_state
from ..enum import Event
from ..ui.base import Element, Layout
from ..ui.layout import Frame, MainFrame


class Handler(QtCore.QObject):
    """Handles QML UI integration with Frame graphical elements.

    Retrieves the graphic elements from the Frame and integrates them with the 
    initial UI elements, and then sets the style of the elements and the Frame 
    in each state.
    """

    def __init__(
            self, gui: QtQuick.QQuickWindow = None, ui: MainFrame = None
            ) -> None:
        """The init receives a QML-based UI and the app's Frame.

        :param gui: QML based UI.
        :param ui: The app's Frame.
        """
        super().__init__()
        self.__gui = gui
        self.__ui = ui
        
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')
        self.__elements = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

        self.__gui.windowStateChanged.connect(self.__state_changed)
        self.__init_state_style()
        self.__integrate_graphic_elements(self.__ui)

    @QtCore.Slot()
    def connections(self):
        """..."""

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
        if Event.MOUSE_RIGHT_PRESS in self.__ui.callbacks():
            self.__ui.callbacks()[Event.MOUSE_RIGHT_PRESS]()

    @QtCore.Slot()
    def __element_clicked(self) -> None:
        # Elements clicked state colors (ignored for now).
        if not self.__main_rect.property('isActive'):
            return

    @QtCore.Slot()
    def __element_pressed(self, element: QtQuick.QQuickItem) -> None:
        # Elements pressed state colors.
        if not self.__main_rect.property('isActive'):
            return

        change_element_style_state(element, ':clicked', self.__ui.style)

    @QtCore.Slot()
    def __element_hover(self, element: QtQuick.QQuickItem) -> None:
        # Elements hover state colors.
        is_active = self.__main_rect.property('isActive')

        if element.property('hovered'):
            state = ':hover' if is_active else ':inactive'
        else:
            state = '' if is_active else ':inactive'

        change_element_style_state(element, state, self.__ui.style)

    def __integrate_graphic_elements(self, layout) -> None:
        # Integration Frame graphic elements into the MainFrame UI.
        for attr, value in layout.__dict__.items():
            if attr.startswith('_') and '__' in attr:
                continue

            element = getattr(layout, attr)
            obj_value = self.__gui.findChild(QtCore.QObject, attr)
            if not obj_value:
                continue
            element._obj = obj_value

            if isinstance(element, Layout):
                self.__integrate_graphic_elements(element)
            
            elif isinstance(element, Element):
                if hasattr(element, 'callbacks'):
                    callbacks = element.callbacks()

                    if Event.MOUSE_PRESS in callbacks:
                        element.connect(
                            callbacks[Event.MOUSE_PRESS], Event.MOUSE_PRESS)
                    elif Event.MOUSE_HOVER in callbacks:
                        element.connect(
                            callbacks[Event.MOUSE_HOVER], Event.MOUSE_HOVER)

        if isinstance(layout, Frame):
            layout._obj = self.__gui

    @QtCore.Slot()
    def __init_state_style(self) -> None:
        # Style of the elements and the Frame in each state.
        if (self.__ui.shape.name == 'MAXIMIZED' or
                self.__ui.shape.name == 'FULL_SCREEN'):
            QtCore.QTimer.singleShot(
                300, lambda: self.__state_changed(QtCore.Qt.WindowFullScreen))
        else:
            self.__state_changed(QtCore.Qt.WindowNoState)

        for child in self.__elements:
            if not child.property('className'):
                continue
            
            if getattr(child, 'clicked', None):
                child.clicked.connect(self.__element_clicked)
            if getattr(child, 'hoveredChanged', None):
                child.hoveredChanged.connect(
                    lambda child=child: self.__element_hover(child))
            if getattr(child, 'pressed', None):
                child.pressed.connect(
                    lambda child=child: self.__element_pressed(child))
            if getattr(child, 'released', None):
                child.released.connect(
                    lambda child=child: self.__element_hover(child))

    @QtCore.Slot()
    def __state_changed(self, state: QtCore.Qt.WindowState) -> None:
        # Frame style in full-screen or normal-screen states.
        if self.__main_rect:
            frame = f'[{self.__ui._name}]'
            if (state == QtCore.Qt.WindowFullScreen
                    or state == QtCore.Qt.WindowMaximized):
                self.__main_rect.setProperty('radiusTopLeft', 0)
                self.__main_rect.setProperty('radiusTopRight', 0)
                self.__main_rect.setProperty('radiusBottomRight', 0)
                self.__main_rect.setProperty('radiusBottomLeft', 0)
                self.__main_rect.setProperty('borderWidth', 0)
                
                self.__main_rect.setProperty('borderWidth', 0)
                self.__main_rect.setProperty('outLineWidth', 0)
                self.__main_rect.setProperty('outLineColor',
                    self.__ui.style[frame]['background_color'])
                self.__main_rect.setProperty('borderColor',
                    self.__ui.style[frame]['background_color'])
                self.__main_rect.setProperty('color',
                    self.__ui.style[frame]['background_color'])
            else:  # QtCore.Qt.WindowNoState
                self.__main_rect.setProperty(
                    'radiusTopLeft', self.__ui.radius[0])
                self.__main_rect.setProperty(
                    'radiusTopRight', self.__ui.radius[1])
                self.__main_rect.setProperty(
                    'radiusBottomRight', self.__ui.radius[2])
                self.__main_rect.setProperty(
                    'radiusBottomLeft', self.__ui.radius[3])
                self.__main_rect.setProperty('borderWidth', 1)
                
                self.__main_rect.setProperty('borderWidth', 1)
                self.__main_rect.setProperty('outLineWidth', 1)
                self.__main_rect.setProperty('outLineColor', '#55000000')
                self.__main_rect.setProperty('borderColor',
                    self.__ui.style[frame]['border_color'])
                self.__main_rect.setProperty('color', "#00000000")

            self.__main_rect.findChild(QtCore.QObject, 'canvas').requestPaint()

    @QtCore.Slot()
    def start_move(self) -> None:
        """Move the apps Frame natively in CSD mode.

        Qt internal method to use native system movement when dragging/moving 
        the application Frame.
        """
        self.__gui.startSystemMove()

    @QtCore.Slot(int)
    def start_resize(self, edge: int) -> None:
        """Resize the app Frame natively in CSD mode.

        Qt's built-in method to use native system resizing in the apps Frame.
        """
        edge = QtCore.Qt.Edge(edge)
        self.__gui.startSystemResize(edge)

    def __str__(self) -> str:
        return "<class 'Handler'>"
