#!/usr/bin/env python3

class UI(object):
    pass


class Add(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    
    def add(self, item: UI) -> UI:
        """..."""
        item._UI__frame = self._UI__frame
        self._QtObject__add(item)

        for x in self._QtObject__items:
            if not x._frame:
                x._UI__frame = self._UI__frame
        return item
