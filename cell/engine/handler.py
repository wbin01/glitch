#/usr/bin/env python3
from cell.ui import AppFrame


class Handler(object):
    """..."""
    def __init__(self) -> None:
        """..."""
        self.__qml_code = None
        self.__app_frame = None
        self.__load_ui_iter = 0
        # ...

    def load_ui(self, app_frame: AppFrame) -> None:
        """..."""
        # TODO: Write qml file
        self.__build_attrs(app_frame)
        self.__build_qml(app_frame)

    def qml_code(self) -> str:
        """..."""
        return self.__qml_code

    def __build_attrs(self, app_frame: AppFrame) -> None:
        for attr, value in app_frame.__dict__.items():
            if not attr.startswith('_'):
                # TODO:
                # obj_value = window.findChild(QtCore.QObject, value.object_id)
                # setattr(self, attr, obj_value)
                setattr(self, attr, attr)

                print('xxxxxxxxxxxxxxx', type(app_frame))
                print(isinstance(app_frame, AppFrame))
                print(attr)
                obj = getattr(app_frame, attr)
                # print(obj, type(obj))

                obj.object_id = attr  # -> app_frame.button.object_id = attr

    def __build_qml(self, app_frame: AppFrame) -> None:
        end = '\n// **closing_key**'
        app_frame.qml, app_close = app_frame.qml.split(end)
        for element in app_frame.added_objects:
            tab = '        ' if self.__load_ui_iter == 0 else '    '

            elm_close = None
            if end in element.qml:
                elm_close = element.qml.split(end)[1]

            if isinstance(element, Layout):
                self.__load_ui_iter += 1
                self.load_ui(element)

            app_frame.qml += '\n'.join(
                [tab + x if x else ''
                for x in element.qml.split(end)[0].split('\n')])

            if elm_close:
                app_frame.qml += elm_close.replace('\n', '\n' + tab)

        self.__qml_code = app_frame.qml + app_close
