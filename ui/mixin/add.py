#!/usr/bin/env python3


class UI(object):
    pass


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def __add_frame(self, layout: None):
        for x in layout._QtObject__items:
            if x._base == 'Layout':
                self.__add_frame(x)

            if not x._UI__frame or x._UI__frame != self._UI__frame:
                x._UI__frame = self._UI__frame
                x._UI__frame_signal.emit()

    
    def add(self, item: UI) -> UI:
        """..."""
        if item not in self._QtObject__items:
            self._QtObject__add(item)

        if self._UI__frame:
            item._UI__frame = self._UI__frame
            item._UI__frame_signal.emit()

        if item._base == 'Layout':
            self.__add_frame(item)

        return item
