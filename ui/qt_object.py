#!/usr/bin/env python3


class UI(object):
    pass


class QtObject(object):
    """..."""
    def __init__(self, name: str = 'Item', *args, **kwargs) -> None:
        self.__name = name
        self.__qml = name + ' {\n    // id\n    // objectName\n    // +\n}'
        self.__obj = None
        self.__items = []
        self.__id = None

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
                    property_ = line.split(':')[-1].strip()  # Convert value
                    if property_.endswith('"') and property_.startswith('"'):
                        return property_.strip('"')
                    return property_
            return None

        property_ = self.__obj.property(name_camel)
        if callable(property_):
            def method(*args, **kwargs):
                return property_(*args, **kwargs)
            return method
        return property_

    def __set_property(self, name, value) -> None:
        if name == 'id':
            self.__id = value.lower()

        if any([name.lower().endswith(x) for x in ['name', 'text', 'source']]):
            if not self.__obj:
                value = '"' + str(value).strip('"').strip("'") + '"'

        # Set Qml obj
        name_camel = self.__snake_to_camel(name)
        if not self.__obj:
            mark = name_camel + ':'

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

    @property
    def qml(self) -> str:
        """..."""
        return self.__qml

    @qml.setter
    def qml(self, qml: str) -> None:
        self.__qml = qml

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
        'anchors__fill'
        if '__' in name:
            name = name.replace('__', '_.')
        name = name.split('_')
        return name[0] + ''.join(x.capitalize() for x in name[1:])
