#!/usr/bin/env python3


class UI(object):
    pass


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def add(self, item: UI) -> UI:
        """..."""
        if item not in self._QtObject__items:
            self._QtObject__add(item)

        if self._UI__frame:
            item._UI__frame = self._UI__frame
            item._UI__frame_signal.emit()

            for x in self._QtObject__items:
                if not x._UI__frame or x._UI__frame != self._UI__frame:
                    x._UI__frame = self._UI__frame
                    x._UI__frame_signal.emit()
                
        return item
