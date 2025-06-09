#/usr/bin/env python3
import sys
import pathlib

from PySide6 import QtCore, QtGui, QtQml, QtQuick

from ..ui.layout import Layout
from ..ui.ui import Ui
from ..ui import Button
import cell._ui as UiObj


style = {
    '[Platform]': {
        'accent_color': '#3c8cbd',
        },
    '[Button]': {
        'background_color': '#333',
        'border_color': '#444',
        'font_color': '#EEE',
        'icon_opacity': 1.0,
        },
    '[Button:inactive]': {
        'background_color': '#222',
        'border_color': '#333',
        'font_color': '#666',
        'icon_opacity': 0.3,
        },
    '[Button:hover]': {
        'background_color': '#383838',
        'border_color': '#883c8cbd',
        'font_color': '#EEE',
        'icon_opacity': 1.0,
        },
    '[Button:clicked]': {
        'background_color': '#333c8cbd',
        'border_color': '#883c8cbd',
        'font_color': '#FFF',
        'icon_opacity': 1.0,
        },
    '[Label]': {
        'font_color': '#EEE',
        },
    '[Label:inactive]': {
        'font_color': '#666',
        },
    '[MainFrame]': {
        'background_color': '#2A2A2A',  # Alt 282828
        'border_color': '#383838',
        'border_radius': 10,
        },
    '[MainFrame:inactive]': {
        'background_color': '#222',
        'border_color': '#333',
        'border_radius': 10,
        },
    }


class GuiEventFilter(QtCore.QObject):
    """..."""
    def __init__(self, main_rect: QtQuick.QQuickItem) -> None:
        """..."""
        super().__init__()
        self.__main_rect = main_rect
        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

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
        self.__main_rect.setProperty(
            'color', style[f'[MainFrame{state}]']['background_color'])
        self.__main_rect.setProperty(
            'borderColor', style[f'[MainFrame{state}]']['border_color'])

        for child in self.__childrens:
            # child.metaObject().className()
            if child.property('qmlType') == 'Label':
                child.setProperty(
                    'color', style[f'[Label{state}]']['font_color'])

            if child.property('qmlType') == 'Button':
                child.findChild(
                    QtCore.QObject, 'buttonBackground').setProperty(
                    'color', style[f'[Button{state}]']['background_color'])
                child.findChild(
                    QtCore.QObject, 'buttonBackground').setProperty(
                    'borderColor', style[f'[Button{state}]']['border_color'])

                child_icon = child.findChild(QtCore.QObject, 'icon')
                child_icon.setProperty(
                    'opacity', style[f'[Button{state}]']['icon_opacity'])

                child_text = child.findChild(QtCore.QObject, 'text')
                child_text.setProperty(
                    'color', style[f'[Button{state}]']['font_color'])


class Handler(QtCore.QObject):
    """..."""
    buttonClicked = QtCore.Signal()

    def __init__(self, gui: QtQuick.QQuickWindow, ui: Ui) -> None:
        """..."""
        super().__init__()
        if not isinstance(gui, QtCore.QObject):
            raise TypeError('Waiting for a root QML QObject')
        
        self.__gui = gui
        self.__ui = ui

        self.__gui.windowStateChanged.connect(self.__gui_state_changed)
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')

        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

        self.__build_state_style()
        self.__build_attrs()

    def __build_state_style(self) -> None:
        for child in self.__childrens:
            if child.property('qmlType') == 'Button':
                button = self.__gui.findChild(
                    QtCore.QObject, child.objectName())

                child.clicked.connect(self.__button_clicked)
                child.hoveredChanged.connect(
                    lambda child=child: self.__button_hover(child))
                child.pressed.connect(
                    lambda child=child: self.__button_pressed(child))
                child.released.connect(
                    lambda child=child: self.__button_hover(child))

    def __build_attrs(self) -> None:
        for attr, value in self.__ui.__dict__.items():
            if not attr.startswith('_'):
                obj_value = self.__gui.findChild(QtCore.QObject, attr)

                if obj_value.property('qmlType') == 'Button':
                    element = UiObj.Button(obj_value)
                elif obj_value.property('qmlType') == 'Label':
                    element = UiObj.Label(obj_value)
                else:
                    element = None

                setattr(self, attr, element)

    @QtCore.Slot()
    def __gui_state_changed(self, state: QtCore.Qt.WindowState) -> None:
        if self.__main_rect:
            if (state & QtCore.Qt.WindowFullScreen
                    or state & QtCore.Qt.WindowMaximized):
                self.__main_rect.setProperty('radius', 0)
                self.__main_rect.setProperty('borderWidth', 0)
                self.__main_rect.setProperty('margins', 0)
            else:  # WindowNoState
                self.__main_rect.setProperty(
                    'radius', style['[MainFrame]']['border_radius'])
                self.__main_rect.setProperty('borderWidth', 1)
                self.__main_rect.setProperty('margins', 1)

    @QtCore.Slot()
    def __button_clicked(self) -> None:
        if self.__main_rect.property('isActive'):
            self.buttonClicked.emit()

    @QtCore.Slot()
    def __button_pressed(self, button: QtQuick.QQuickItem) -> None:
        if self.__main_rect.property('isActive'):
            button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
                'color', style['[Button:clicked]']['background_color'])
            button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
                'borderColor', style['[Button:clicked]']['border_color'])

            button_text = button.findChild(QtCore.QObject, 'text')
            button_text.setProperty(
                'color', style['[Button:clicked]']['font_color'])

    @QtCore.Slot()
    def __button_hover(self, button: QtQuick.QQuickItem) -> None:
        is_active = self.__main_rect.property('isActive')

        if button.property('hovered'):
            state = ':hover' if is_active else ':inactive'
        else:
            state = '' if is_active else ':inactive'

        button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
            'color', style[f'[Button{state}]']['background_color'])
        button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
            'borderColor', style[f'[Button{state}]']['border_color'])

        button_text = button.findChild(QtCore.QObject, 'text')
        button_text.setProperty(
            'color', style[f'[Button{state}]']['font_color'])

    @QtCore.Slot()
    def start_move(self) -> None:
        """..."""
        self.__gui.startSystemMove()

    @QtCore.Slot(int)
    def start_resize(self, edge: int) -> None:
        """..."""
        edge = QtCore.Qt.Edge(edge)
        self.__gui.startSystemResize(edge)


class Application(object):
    """..."""
    def __init__(self, ui: Ui) -> None:
        """..."""
        self.__ui = ui
        self.__handler = None

        self.__qml_code = None
        self.__load_ui_iter = 0
        self.__load_ui()

        self.__qt_gui_application = QtGui.QGuiApplication(sys.argv)
        self.engine = QtQml.QQmlApplicationEngine()
        self.engine.load(
            pathlib.Path(__file__).parent.parent /'static'/'qml'/'main.qml')

        if not self.engine.rootObjects():
            sys.exit(-1)

        self.__gui = self.engine.rootObjects()[0]
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')

    @property
    def handler(self) -> None:
        """..."""
        return self.__handler

    @handler.setter
    def handler(self, handler: Handler) -> None:
        self.__handler = handler

    @property
    def ui(self) -> None:
        """..."""
        return self.__ui

    @ui.setter
    def ui(self, ui) -> None:
        self.__ui = ui

    @property
    def gui(self) -> QtQuick.QQuickWindow:
        """..."""
        return self.__gui

    @gui.setter
    def gui(self, gui: QtQuick.QQuickWindow) -> None:
        self.__gui = gui

    def exec(self) -> None:
        """..."""
        event_filter = GuiEventFilter(self.__main_rect)
        self.__gui.installEventFilter(event_filter)

        self.engine.rootContext().setContextProperty('logic', self.__handler)
        sys.exit(self.__qt_gui_application.exec())

    def __load_ui(self) -> None:
        # button_press.object_id = "button_press"
        for attr, value in self.__ui.__dict__.items():
            if not attr.startswith('_'):
                getattr(self.__ui, attr).object_id = attr

        self.__load_ui_build_qml()

        qml = pathlib.Path(__file__).parent.parent /'static'/'qml'/'main.qml'
        qml.write_text(self.__qml_code)

    def __load_ui_build_qml(self) -> None:
        end = '\n// **closing_key**'
        self.__ui.qml, ui_close = self.__ui.qml.split(end)
        for element in self.__ui.added_objects:
            tab = ' ' * 12 if self.__load_ui_iter == 0 else '    '

            elm_close = None
            if end in element.qml:
                elm_close = element.qml.split(end)[1]

            if isinstance(element, Layout):
                self.__load_ui_iter += 1
                self.__load_ui(element)

            self.__ui.qml += '\n'.join(
                [tab + x if x else ''
                for x in element.qml.split(end)[0].split('\n')])

            if elm_close:
                self.__ui.qml += elm_close.replace('\n', '\n' + tab)

        self.__qml_code = self.__ui.qml + ui_close
