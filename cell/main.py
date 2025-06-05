#/usr/bin/env python3
import sys
import textwrap

from PySide6 import QtCore, QtGui, QtQml, QtQuick


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


class MainFrameEventFilter(QtCore.QObject):
    def __init__(self, main_rect):
        super().__init__()
        self.__main_rect = main_rect
        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

    def eventFilter(self, obj, event):
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


class AppLogic(QtCore.QObject):
    """..."""
    buttonClicked = QtCore.Signal()

    def __init__(self, window) -> None:
        """..."""
        super().__init__()
        if not isinstance(window, QtCore.QObject):
            raise TypeError('Waiting for a root QML QObject')
        
        self.__window = window
        self.__window.windowStateChanged.connect(self.__window_state_changed)

        self.__main_rect = self.__window.findChild(QtCore.QObject, 'mainRect')

        self.__childrens = self.__main_rect.findChildren(
            QtCore.QObject, options=QtCore.Qt.FindChildrenRecursively)

        for child in self.__childrens:
            if child.property('qmlType') == 'Button':
                button = self.__window.findChild(
                    QtCore.QObject, child.objectName())

                child.clicked.connect(self.__button_clicked)
                child.hoveredChanged.connect(
                    lambda child=child: self.__button_hover(child))
                child.pressed.connect(
                    lambda child=child: self.__button_pressed(child))
                child.released.connect(
                    lambda child=child: self.__button_hover(child))

    @QtCore.Slot()
    def __window_state_changed(self, state) -> None:
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
    def __button_pressed(self, button) -> None:
        if self.__main_rect.property('isActive'):
            button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
                'color', style['[Button:clicked]']['background_color'])
            button.findChild(QtCore.QObject, 'buttonBackground').setProperty(
                'borderColor', style['[Button:clicked]']['border_color'])

            button_text = button.findChild(QtCore.QObject, 'text')
            button_text.setProperty(
                'color', style['[Button:clicked]']['font_color'])

    @QtCore.Slot()
    def __button_hover(self, button) -> None:
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
        self.__window.startSystemMove()

    @QtCore.Slot(int)
    def start_resize(self, edge: int) -> None:
        edge = QtCore.Qt.Edge(edge)
        self.__window.startSystemResize(edge)

if __name__ == "__main__":
    app = QtGui.QGuiApplication(sys.argv)
    engine = QtQml.QQmlApplicationEngine()

    engine.load("cell/main.qml")
    if not engine.rootObjects():
        sys.exit(-1)

    window = engine.rootObjects()[0]
    main_rect = window.findChild(QtCore.QObject, 'mainRect')
    event_filter = MainFrameEventFilter(main_rect)
    window.installEventFilter(event_filter)

    logic = AppLogic(window)
    engine.rootContext().setContextProperty('logic', logic)

    sys.exit(app.exec())
