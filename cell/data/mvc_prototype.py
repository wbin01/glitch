#/usr/bin/env python3
class Layout(object):
    """..."""
    pass

class Element(object):
    """..."""
    pass

class Layout(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__id = str(id(self))
        self.__qml = self.__id
        self.__added_objects = []

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__qml = self.__qml.replace(f'id: {self.__id}', f'id: {object_id}')
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

    @property
    def added_objects(self) -> list:
        """..."""
        return self.__added_objects

    @added_objects.setter
    def added_objects(self, added_objects: list) -> None:
        self.__added_objects = added_objects

    def add(self, obj) -> Layout | Element:
        """..."""
        self.__added_objects.append(obj)
        return obj


class Element(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        self.__id = str(id(self))
        self.__qml = self.__id

    @property
    def object_id(self) -> str:
        """..."""
        return self.__id

    @object_id.setter
    def object_id(self, object_id: str) -> None:
        self.__qml = self.__qml.replace(f'id: {self.__id}', f'id: {object_id}')
        self.__id = object_id

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml


class AppFrame(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__('appFrame', *args, **kwargs)
        self.object_id = 'appFrame'
        self.qml = (
            'AppFrame {'
            f'\n    id: appFrame\n'
            '\n    Rectangle {'
            '\n        id: mainRect'
            '\n// **closing_key**'
            '\n    }  // Rectangle id: mainRect'
            '\n}  // AppFrame id: appFrame')
        self.added_objects = []


class Box(Layout):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.qml = (
            '\n'
            '\nBox {'
            f'\n    id: {self.object_id}'
            '\n// **closing_key**'
            f'\n}}  // Box id: {self.object_id}')
        self.added_objects = []


class Button(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.qml = (
            '\n'
            '\nButton {'
            f'\n    id: {self.object_id}'
            '\n// **closing_key**'
            f'\n}}  // Button id: {self.object_id}')


class Label(Element):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.qml = (
            '\n'
            '\nLabel {'
            f'\n    id: {self.object_id}'
            '\n// **closing_key**'
            f'\n}}  // Label id: {self.object_id}')


class Model(object):
    """..."""
    # SqLite data model (Optional use)
    pass


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

                obj = getattr(app_frame, attr)
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


class Application(object):
    """..."""
    def __init__(self, controller) -> None:
        """..."""
        self.__controller = controller
        # ...

    def exec(self):
        """..."""
        print(self.__controller.qml_code())


if __name__ == '__main__':
    class View(AppFrame):
        def __init__(self, *args, **kwargs) -> None:
            super().__init__(*args, **kwargs)
            
            button0 = self.add(Button())
            # button0.object_id = 'button0'
            label = self.add(Label())

            box1 = self.add(Box())
            self.button1 = box1.add(Button())
            # self.button1.object_id = 'button1'
            label1 = box1.add(Label())

            box2 = box1.add(Box())
            label2 = box2.add(Label())


    class Handles(Handler):
        def __init__(self) -> None:
            super().__init__()
            self.load_ui(View())
            
            print(self.button1)


    app = Application(Handles())
    app.exec()
