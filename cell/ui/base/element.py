#/usr/bin/env python3
from .ui import UI


class Element(UI):
    """A visual element object.

    Elements are visual and interactive application items such as buttons and 
    text.
    """
    def __init__(self, *args, **kwargs) -> None:
        """..."""
        super().__init__(*args, **kwargs)
        self.id = '_' + str(id(self))
        self._element_type = 'Element'

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
        margins = {
            'topMargin': 0, 'rightMargin': 0,
            'bottomMargin': 0, 'leftMargin': 0}

        for line in self._qml.split('\n'):
            for margin in margins:
                if 'property int ' + margin in line:
                    margins[margin] = int(line.split(':')[-1].strip())
        
        return (
            margins['topMargin'], margins['rightMargin'],
            margins['bottomMargin'], margins['leftMargin'])

    @margins.setter
    def margins(self, margins: tuple) -> None:
        if isinstance(margins, str):
            if not margins.isdigit():
                return
            margins = int(magins)

        prev_margins = self.margins

        if isinstance(margins, int):
            top, right, bottom, left = margins, margins, margins, margins
        elif len(margins) == 2:
            top, right, bottom, left = margins + (margins[1], margins[1])
        elif len(margins) == 3:
            top, right, bottom, left = margins + (margins[2],)
        else:
            top, right, bottom, left = margins[:4]

        top = prev_margins[0] if top is None else top
        right = prev_margins[1] if right is None else right
        bottom = prev_margins[2] if bottom is None else bottom
        left = prev_margins[3] if left is None else left

        qml = []
        for line in self._qml.split('\n'):
            if 'property int topMargin:' in line:
                qml.append(f'property int topMargin: {top}')
            elif 'property int rightMargin:' in line:
                qml.append(f'property int rightMargin: {right}')
            elif 'property int bottomMargin:' in line:
                qml.append(f'property int bottomMargin: {bottom}')
            elif 'property int leftMargin:' in line:
                qml.append(f'property int leftMargin: {left}')
            else:
                qml.append(line)
        self._qml = '\n'.join(qml)
