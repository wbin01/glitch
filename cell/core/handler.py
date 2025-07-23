#/usr/bin/env python3
from PySide6 import QtCore, QtQuick

from .tools import change_element_style_state
from .. import gui
from ..enum.event import Event
from ..ui.main_frame import MainFrame


class Handler(QtCore.QObject):
    """..."""

    def __init__(
            self, gui: QtQuick.QQuickWindow = None, ui: MainFrame = None
            ) -> None:
        """..."""
        super().__init__()
        self.__gui = gui
        self.__ui = ui
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')
        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

        self.__gui.windowStateChanged.connect(self.__gui_state_changed)

        self.__element_properties = {
            'color': 'font_color',
            'backgroundColor': 'background_color',
            'borderColor': 'border_color',
            'text': {
                'color': 'font_color'},
            'background': {
                'backgroundColor': 'background_color',
                'borderColor': 'border_color'},
            'icon': {
                'opacity': 'icon_opacity'},
            }
        self.__build_state_style()
        self.__build_attrs(self.__ui)

    def __build_state_style(self) -> None:
        for child in self.__childrens:
            if child.property('qmlType') in ['Button']:
                # button = self.__gui.findChild(
                #     QtCore.QObject, child.objectName())

                child.clicked.connect(self.__element_clicked)
                child.hoveredChanged.connect(
                    lambda child=child: self.__element_hover(child))
                child.pressed.connect(
                    lambda child=child: self.__element_pressed(child))
                child.released.connect(
                    lambda child=child: self.__element_hover(child))

    def __build_attrs(self, layout) -> None:
        elements = {
            'Button': gui.Button, 'Label': gui.Label,
            'ScrollBox': gui.ScrollBox,
            }

        for attr, value in layout.__dict__.items():
            if attr.startswith('_'):
                continue

            obj_value = self.__gui.findChild(QtCore.QObject, attr)
            if not obj_value:
                continue

            element_name = obj_value.property('qmlType')
            if element_name in elements:
                gui_element = elements[element_name](obj_value)
            else:
                gui_element = None

            ui_element = getattr(layout, attr)
            if hasattr(ui_element, 'callbacks'):
                if Event.MOUSE_PRESS in ui_element.callbacks:
                    gui_element.connect(
                        ui_element.callbacks[Event.MOUSE_PRESS])

            setattr(layout, attr, gui_element)
            setattr(self, attr, gui_element)

    @QtCore.Slot()
    def __gui_state_changed(self, state: QtCore.Qt.WindowState) -> None:
        # Fullscreen borders
        if self.__main_rect:
            if (state & QtCore.Qt.WindowFullScreen
                    or state & QtCore.Qt.WindowMaximized):
                self.__main_rect.setProperty('radius', 0)
                self.__main_rect.setProperty('borderWidth', 0)
                self.__main_rect.setProperty('margins', 0)
            else:  # WindowNoState
                self.__main_rect.setProperty(
                    'radius',
                    self.__ui.style['[MainFrame]']['border_radius'])
                self.__main_rect.setProperty('borderWidth', 1)
                self.__main_rect.setProperty('margins', 1)

    @QtCore.Slot()
    def __element_clicked(self) -> None:
        if not self.__main_rect.property('isActive'):
            return

    @QtCore.Slot()
    def __element_pressed(self, element: QtQuick.QQuickItem) -> None:
        # Elements pressed state colors
        if not self.__main_rect.property('isActive'):
            return

        change_element_style_state(element, ':clicked', self.__ui.style)

    @QtCore.Slot()
    def __element_hover(self, element: QtQuick.QQuickItem) -> None:
        # Elements hover state colors
        is_active = self.__main_rect.property('isActive')

        if element.property('hovered'):
            state = ':hover' if is_active else ':inactive'
        else:
            state = '' if is_active else ':inactive'

        change_element_style_state(element, state, self.__ui.style)

    @QtCore.Slot()
    def start_move(self) -> None:
        """..."""
        self.__gui.startSystemMove()

    @QtCore.Slot(int)
    def start_resize(self, edge: int) -> None:
        """..."""
        edge = QtCore.Qt.Edge(edge)
        self.__gui.startSystemResize(edge)
