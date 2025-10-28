#!/usr/bin/env python3


class UI(object):
    pass


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __add_app(self, layout: None):
        for x in layout._QtObject__items:
            if x._base == 'Layout':
                self.__add_app(x)

            if not x._UI__app or x._UI__app != self._UI__app:
                x._UI__app = self._UI__app
                x._UI__app_signal.emit()

    
    def add(self, item: UI) -> UI:
        """..."""
        if item not in self._QtObject__items:
            self._QtObject__add(item)

        if self._UI__app:
            item._UI__app = self._UI__app
            item._UI__app_signal.emit()

            if item._base == 'Layout':
                self.__add_app(item)

        return item
