#/usr/bin/env python3
import pathlib

from PySide6 import QtCore

from cell.ui import AppFrame
from cell.ui.layout import Layout


class Handler(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__app = None
        self.__qml_code = None
        self.__app_frame = None
        self.__load_ui_iter = 0

    def _build_attrs(self, app):
        if self.__app_frame:
            for attr, value in self.__app_frame.__dict__.items():
                if not attr.startswith('_'):
                    obj_value = app.findChild(QtCore.QObject, attr)
                    print(obj_value)
                    print(attr)
                    setattr(self, attr, obj_value)

    def load_ui(self, app_frame: AppFrame) -> None:
        """..."""
        self.__app_frame = app_frame

        # button_press.object_id = "button_press"
        for attr, value in self.__app_frame.__dict__.items():
            if not attr.startswith('_'):
                getattr(self.__app_frame, attr).object_id = attr

        self.__build_qml()

        qml_path = pathlib.Path(__file__).parent.parent / 'qml' / 'main.qml'
        qml_path.write_text(self.__qml_code)
        # qml_path.parent.mkdir(parents=True, exist_ok=True)
        # qml_path.exists()

    def qml_code(self) -> str:
        """..."""
        return self.__qml_code

    def __build_qml(self) -> None:
        end = '\n// **closing_key**'
        self.__app_frame.qml, app_close = self.__app_frame.qml.split(end)
        for element in self.__app_frame.added_objects:
            tab = ' ' * 12 if self.__load_ui_iter == 0 else '    '

            elm_close = None
            if end in element.qml:
                elm_close = element.qml.split(end)[1]

            if isinstance(element, Layout):
                self.__load_ui_iter += 1
                self.load_ui(element)

            self.__app_frame.qml += '\n'.join(
                [tab + x if x else ''
                for x in element.qml.split(end)[0].split('\n')])

            if elm_close:
                self.__app_frame.qml += elm_close.replace('\n', '\n' + tab)

        self.__qml_code = self.__app_frame.qml + app_close
