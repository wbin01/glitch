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
        self._element_type = 'Element'
        
        self.__fill_height = False
        self.__fill_width = True
        self.__height = 30
        self.__width = 100
        self.__size = self.__width, self.__height
        
        self.__margins = 0, 0, 0, 0        

    @property
    def margins(self) -> tuple:
        """Sets the `Button` margins.

        A tuple with the 4 margin values. The values are in clockwise
        order: top, right, bottom and left respectively.

        Get:
            (5, 10, 5, 10)

        Set:
            It is not mandatory to pass all the values, the last value will be 
            used to fill in the missing ones:

            `margins = 5` is equivalent to `margins = 5, 5, 5, 5`
            `margins = 5, 10` is equivalent to `margins = 5, 10, 10, 10`

            Use `None` for a value to be automatic. `None` indicates that the 
            value is the same as before. Example:

                # Change vertical margins (top and bottom)
                `element.margins = 10, None, 10, None`

                # Change horizontal margins (right and left)
                `element.margins = None, 5, None, 5`
        """
        return self.__margins

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            if not margins.isdigit():
                return
            margins = int(margins)

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = self.__margins[0] if top is None else top
        right = self.__margins[1] if right is None else right
        bottom = self.__margins[2] if bottom is None else bottom
        left = self.__margins[3] if left is None else left

        if self._obj:
            self._obj.setProperty('topMargin', top)
            self._obj.setProperty('rightMargin', right)
            self._obj.setProperty('bottomMargin', bottom)
            self._obj.setProperty('leftMargin', left)
        else:
            self._qml = self._qml.replace(
                f'property int topMargin: {self.__margins[0]}',
                f'property int topMargin: {top}')
            self._qml = self._qml.replace(
                f'property int rightMargin: {self.__margins[1]}',
                f'property int rightMargin: {right}')
            self._qml = self._qml.replace(
                f'property int bottomMargin: {self.__margins[2]}',
                f'property int bottomMargin: {bottom}')
            self._qml = self._qml.replace(
                f'property int leftMargin: {self.__margins[3]}',
                f'property int leftMargin: {left}')

        self.__margins = top, left, bottom, right

    @property
    def size(self) -> tuple:
        """Frame width and height.

        Tuple like (500, 500).
        """
        return self.__size

    @size.setter
    def size(self, size: tuple) -> None:
        if not isinstance(size, int) and not isinstance(size, tuple):
            logging.error(
                f'\n  {self._element_type}.size: Use a tuple of integers like '
                '(100, 30) or an integer like 500.')
            return

        if isinstance(size, int):
            width, height = size, size
        elif len(size) == 1:
            width, height = size[0], size[0]
        elif len(size) >= 2:
            width, height = size[:2]

        enum_w = width if isinstance(width, Size) else False
        enum_h = height if isinstance(height, Size) else False
        width = self.__size[0] if not isinstance(width, int) else width
        height = self.__size[1] if not isinstance(height, int) else height

        if self._obj:
            # self._obj.setProperty('_width', width)
            # self._obj.setProperty('_height', height)
            pass
        else:
            self.__set_size(enum_w, 'width', width)
            self.__set_size(enum_h, 'height', height)

        self.__width = width
        self.__height = height
        self.__size = width, height

    def __set_size(
            self, enum: Size, width_height: 'width', value: int) -> None:
        fill = 'fillWidth' if width_height == 'width' else 'fillHeight'
        w_h = f'_{width_height}'
        new_value = value
        last_value = self.__width if width_height == 'width' else self.__height

        if enum:
            if enum.value == 'FILL':
                self._qml = self._qml.replace(
                    f'{fill}: false', f'{fill}: true')

            elif f'property bool {fill}: false' in self._qml:
                self._qml = self._qml.replace(
                    f'{w_h}: {last_value}', f'{w_h}: {new_value}')
        else:
            self._qml = self._qml.replace(
                f'{fill}: true', f'{fill}: false').replace(
                    f'{w_h}: {last_value}', f'{w_h}: {new_value}')

    def __str__(self) -> str:
        return "<class 'Element'>"
