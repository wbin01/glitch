#/usr/bin/env python3
import sys
import pathlib

from PySide6 import QtCore, QtGui, QtQml, QtQuick

from ..ui.layout import Layout
from ..ui.main_frame import MainFrame
from cell import gui


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
        self.__build_state_style()
        self.__build_attrs(self.__ui)

    def __build_state_style(self) -> None:
        for child in self.__childrens:
            if child.property('qmlType') == 'Button':
                # button = self.__gui.findChild(
                #     QtCore.QObject, child.objectName())

                child.clicked.connect(self.__button_clicked)
                child.hoveredChanged.connect(
                    lambda child=child: self.__button_hover(child))
                child.pressed.connect(
                    lambda child=child: self.__button_pressed(child))
                child.released.connect(
                    lambda child=child: self.__button_hover(child))

    def __build_attrs(self, layout) -> None: 
        for attr, value in layout.__dict__.items():
            if attr.startswith('_'):
                continue

            obj_value = self.__gui.findChild(QtCore.QObject, attr)
            if not obj_value:
                continue

            if obj_value.property('qmlType') == 'Button':
                gui_element = gui.Button(obj_value)
            elif obj_value.property('qmlType') == 'Label':
                gui_element = gui.Label(obj_value)
            elif obj_value.property('qmlType') == 'ScrollBox':
                gui_element = gui.ScrollBox(obj_value)
                self.__build_attrs(gui_element)
            else:
                gui_element = None

            ui_element = getattr(layout, attr)
            if hasattr(ui_element, 'callables'):
                if 'clicked' in ui_element.callables:
                    gui_element.connect(ui_element.callables['clicked'])

            setattr(layout, attr, gui_element)
            setattr(self, attr, gui_element)

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
    def __init__(
            self, app_frame: MainFrame = MainFrame, handler: Handler = Handler
            ) -> None:
        """..."""
        self.__ui = app_frame()
        self.__path = pathlib.Path(__file__).parent.parent

        self.__qml_code = None
        self.__qml_code_iterator = 0
        self.__qml_path = self.__path /'static'/'qml'/'main.qml'
        self.__write_qml_code(self.__ui)

        self.__qt_gui_application = QtGui.QGuiApplication(sys.argv)
        self.__engine = QtQml.QQmlApplicationEngine()
        self.__engine.load(self.__qml_path)
        if not self.__engine.rootObjects():
            sys.exit(-1)

        self.__gui = self.__engine.rootObjects()[0]
        self.__main_rect = self.__gui.findChild(QtCore.QObject, 'mainRect')

        self.__handler = handler(self.__gui, self.__ui)

    def app_frame(self) -> Handler:
        """..."""
        return self.__ui

    def exec(self) -> None:
        """..."""
        event_filter = GuiEventFilter(self.__main_rect)
        self.__gui.installEventFilter(event_filter)

        self.__engine.rootContext().setContextProperty('logic', self.__handler)
        sys.exit(self.__qt_gui_application.exec())

    def __write_qml_code(self, layout) -> None:
        for attr, value in layout.__dict__.items():
            if not attr.startswith('_'):
                getattr(layout, attr).object_id = attr

        self.__load_ui_build_qml(layout)
        self.__qml_path.write_text(self.__qml_code)

    def __load_ui_build_qml(self, layout) -> None:
        end = '\n// **closing_key**'
        layout.qml, ui_close = layout.qml.split(end)
        for element in layout.added_objects:
            tab = ' ' * 12 if self.__qml_code_iterator == 0 else '    '

            elm_close = None
            if end in element.qml:
                elm_close = element.qml.split(end)[1]

            if isinstance(element, Layout):
                self.__qml_code_iterator += 1
                self.__write_qml_code(element)

            layout.qml += '\n'.join(
                [tab + x if x else ''
                for x in element.qml.split(end)[0].split('\n')])

            if elm_close:
                layout.qml += elm_close.replace('\n', '\n' + tab)

        self.__qml_code = layout.qml + ui_close
