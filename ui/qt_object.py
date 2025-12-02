#!/usr/bin/env python3


class UI(object):
    pass


class QtObject(object):
    """..."""
    def __init__(self, name: str = 'Item', *args, **kwargs) -> None:
        qml = name + ' {\n    id: <id>\n    objectName: "<id>"\n    // +\n}'

        self.__name = name
        self.__qml = qml
        self.__obj = None
        self.__items = []
        self.__id = None
        self.__layout_types = (
            'layout.Layout', 'frame.Frame', 'header.Header',
            'control_buttons.ControlButtons')

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(name={self.__name!r})'

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(name={self.__name!r})'

    def __property(self, name: str):
        if name == 'id' and self.__id:
            return self.__id

        name_camel = self.__snake_to_camel(name)
        if not self.__obj:
            mark = name_camel + ':'

            if not mark in self.__qml:
                return None

            for line in self.__qml.split('\n'):
                if mark in line:
                    prop = line.split(':')[-1].strip()
                    if prop.endswith('"') and prop.startswith('"'):
                        prop = prop.strip('"')

                    if prop.isdigit():
                        prop = int(prop)
                    elif '.' in prop and prop.replace('.', '').isdigit():
                        prop = float(prop)
                    elif prop == 'true' or prop == 'false':
                        prop = True if prop == 'true' else False
                    return prop

            return None

        prop = self.__obj.property(name_camel)
        if callable(prop):
            def method(*args, **kwargs):
                return prop(*args, **kwargs)
            return method
        return prop

    def __set_property(self, name, value) -> None:
        if name == 'id':
            self.__id = value.lower()

        if any([name.lower().endswith(x) for x in ['name', 'text', 'source']]):
            if not self.__obj:
                value = '"' + str(value).strip('"').strip("'") + '"'

        if name.lower().endswith('color') and value.startswith('#'):
            if not self.__obj:
                value = '"' + str(value).strip('"').strip("'") + '"'

        # Set Qml obj
        name_camel = self.__snake_to_camel(name)
        if not self.__obj:
            mark = name_camel + ':'

            if isinstance(value, bool):
                value = 'true' if value else 'false'

            # Create qml property
            new_qml = ''
            if not mark in self.__qml:
                for line in self.__qml.split('\n'):
                    if '// +' in line:
                        space, _ = line.split('// +')
                        new_qml += f'{space}{name_camel}: {value}\n'
                        new_qml += space + '// +\n'
                    else:
                        if line:
                            new_qml += f'{line}\n'
                self.__qml = new_qml
                return

            # Update qml property
            for line in self.__qml.split('\n'):
                if mark in line:
                    new_qml += f'{line.split(':')[0]}: {value}\n'
                else:
                    if line:
                        new_qml += f'{line}\n'

            self.__qml = new_qml
            return

        # Apply Qobj
        self.__obj.setProperty(name_camel, value)

    def __insert_code(self, code) -> None:
        new_qml = ''
        for line in self.__qml.split('\n'):
            if '// code' in line:
                space, _ = line.split('// code')
                new_qml += f'{space}{code}\n'
                new_qml += space + '// code\n'
            else:
                if line:
                    new_qml += f'{line}\n'
        self.__qml = new_qml

    @property
    def _name(self) -> str:
        """..."""
        return self.__name

    def __add(self, item: UI) -> UI:
        """..."""
        self.__items.append(item)
        return item

    @staticmethod
    def __snake_to_camel(name: str) -> str:
        name = name.split('_')
        return name[0] + ''.join(x.capitalize() for x in name[1:])
