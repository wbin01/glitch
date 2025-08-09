#!/usr/bin/env python3
import logging

from ...enum import Size
from .ui import UI


class Element(UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.__fill_height = False
        self.__fill_width = True
        self.__height = 30
        self.__width = 100
        self.__size = self.__width, self.__height
        self.__margins = 0, 0, 0, 0

        self.class_id('Element')

    @property
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        A tuple with the 4 margin values. The values are in clockwise
        order: top, right, bottom and left respectively.

            (5, 10, 5, 10)

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `margins = 5` is equivalent to `margins = 5, 5, 5, 5`
        `margins = 5, 10` is equivalent to `margins = 5, 10, 10, 10`

        Any value other than an `int`, such as `None` or `Size.AUTO`, will 
        be handled automatically, using the old value.

            # Change vertical margins (top and bottom)
            `margins = 10, None, 10, None`

            # Change horizontal margins (right and left)
            `margins = Size.AUTO, 5, Size.AUTO, 5`
        """
        return self.__margins

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if not isinstance(margins, int) and not isinstance(margins, tuple):
            logging.error(
                f'\n  {self._name}.margins: Use a tuple of integers like '
                '(10, 10, 10, 10) or an integer like 10.')
            return

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = self.__margins[0] if not isinstance(top, int) else top
        right = self.__margins[1] if not isinstance(right, int) else right
        bottom = self.__margins[2] if not isinstance(bottom, int) else bottom
        left = self.__margins[3] if not isinstance(left, int) else left

        if self._obj:
            self._obj.setProperty('topMargin', top)
            self._obj.setProperty('rightMargin', right)
            self._obj.setProperty('bottomMargin', bottom)
            self._obj.setProperty('leftMargin', left)
        else:
            self._qml = self._qml.replace(
                f'topMargin: {self.__margins[0]}', f'topMargin: {top}')
            self._qml = self._qml.replace(
                f'rightMargin: {self.__margins[1]}', f'rightMargin: {right}')
            self._qml = self._qml.replace(
                f'bottomMargin: {self.__margins[2]}',f'bottomMargin: {bottom}')
            self._qml = self._qml.replace(
                f'leftMargin: {self.__margins[3]}', f'leftMargin: {left}')

        self.__margins = top, left, bottom, right

    @property
    def size(self) -> tuple:
        """Frame width and height.

        Tuple like (100, 30).

        It is not mandatory to pass all the values, the last value will be 
        used to fill in the missing ones:

        `size = 100` is equivalent to `margins = 100, 100`

        Use `Size.AUTO` enum (or `None`) for a value to be automatic.
        `Size.AUTO` indicates that the value is the same as before. Example:

            # Change only the height
            `size = Size.AUTO, 50

            # Change only the width
            `size = 100, Size.AUTO

        Use `Size.FILL` to completely fill the space. Example:

            # Horizontal fill
            `size = Size.FILL, 30

            # Vertical fill
            `size = 100, Size.FILL
        """
        return self.__size

    @size.setter
    def size(self, size: tuple) -> None:
        if not isinstance(size, int) and not isinstance(size, tuple):
            logging.error(
                f'\n  {self._name}.size: Use a tuple of integers like '
                '(100, 30) or an integer like 500.')
            return

        if isinstance(size, int):
            width, height = size, size
        elif len(size) == 1:
            width, height = size[0], size[0]
        elif len(size) >= 2:
            width, height = size[:2]

        width = Size.AUTO if width is None else width
        height = Size.AUTO if height is None else height

        enum_w = width if isinstance(width, Size) else False
        enum_h = height if isinstance(height, Size) else False
        width = self.__size[0] if not isinstance(width, int) else width
        height = self.__size[1] if not isinstance(height, int) else height

        if self._obj:
            self.__set_obj_size(enum_w, 'width', width)
            self.__set_obj_size(enum_h, 'height', height)
        else:
            self.__set_qml_size(enum_w, 'width', width)
            self.__set_qml_size(enum_h, 'height', height)

        self.__width = width
        self.__height = height
        self.__size = width, height

    def __set_obj_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        if enum:
            if enum == Size.FILL:
                self._obj.setProperty(fill, True)

            elif not self._obj.property(fill):
                self._obj.setProperty(width_height, value)
        else:
            self._obj.setProperty(fill, False)
            self._obj.setProperty(width_height, value)

    def __set_qml_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        old_value = self.__width if width_height == 'width' else self.__height

        if enum:
            if enum == Size.FILL:
                self._qml = self._qml.replace(f'{fill}: false',f'{fill}: true')

            elif f'property bool {fill}: false' in self._qml:
                self._qml = self._qml.replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')
        else:
            self._qml = self._qml.replace(
                f'{fill}: true', f'{fill}: false').replace(
                    f'{width_height}: {old_value}', f'{width_height}: {value}')

    def __str__(self) -> str:
        return "<class 'Element'>"
