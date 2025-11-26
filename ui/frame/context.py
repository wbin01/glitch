#!/usr/bin/env python3
from PySide6.QtCore import QTimer

from .frame import Frame
from ...enum.hint import Hint


class Context(Frame):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._UI__app = self
        self.__height = 0
        self.visible = False

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def visible(self) -> bool:
        """..."""
        value = self._QtObject__property('visibility').value
        return False if not value else True

    @visible.setter
    def visible(self, value: str) -> None:
        value = 'Window.Windowed' if value else 'Window.Hidden'
        self._QtObject__set_property('visibility', value)

    def open(
            self, x: int = 0, y: int = 0,
            height: int = 30, width: int = 100) -> None:
        """..."""
        self.__height = 0
        if self._QtObject__obj:
            self.height = height if height else self.__get_height(self)
            self.width = width if width else int(self.width[0]) + 2

            QTimer.singleShot(100, lambda: self.__pos(x, y))
            self._QtObject__obj.show()
    
    def __get_height(self, frame: Frame) -> int:
        if len(frame._QtObject__items) > 1:
            self.__height += frame.spacing

        for element in frame._QtObject__items:
            if element._base == 'View':
                self.__height += element.height[0]
                self.__height += element.margin[0]
                self.__height += element.margin[2]

            element_items = (getattr(element, '_QtObject__items')
                if hasattr(element, '_QtObject__items') else None)

            if element_items and isinstance(element_items, list):
                self.__get_height(element)

        return int(self.__height) + 2

    def __pos(self, x: int, y: int) -> None:
        self._QtObject__obj.x = x
        self._QtObject__obj.y = y
