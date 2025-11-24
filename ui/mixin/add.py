#!/usr/bin/env python3


class UI(object):
    pass


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.spacing = 6

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def spacing(self) -> int:
        """..."""
        return self._QtObject__property('spacing')

    @spacing.setter
    def spacing(self, spacing: int) -> None:
        self._QtObject__set_property('spacing', spacing)

    def add(self, item: UI) -> UI:
        """..."""
        return self.__add(item)

    def __add(self, item: UI) -> UI:
        """..."""
        qml_base = f'_{item.__class__.__name__}__qml_base'
        if (item._base == 'Frame' and
                hasattr(item, qml_base) and
                getattr(item, qml_base) == 'Context'):
            item.visible = False

        if item not in self._QtObject__items:
            self._QtObject__add(item)

        if self._UI__app:
            item._UI__app = self._UI__app
            item._UI__app_signal.emit()

            qml_base = f'_{item.__class__.__name__}__qml_base'
            if (item._base == 'Layout' or
                    hasattr(item, qml_base) and
                    getattr(item, qml_base) == 'Layout'):
                self.__add_app(item)

        return item
    
    def __add_app(self, layout: None):
        for x in layout._QtObject__items:
            qml_base = f'_{x.__class__.__name__}__qml_base'
            if (x._base == 'Layout' or
                    hasattr(x, qml_base) and
                    getattr(x, qml_base) == 'Layout'):
                self.__add_app(x)

            if not x._UI__app or x._UI__app != self._UI__app:
                x._UI__app = self._UI__app
                x._UI__app_signal.emit()
