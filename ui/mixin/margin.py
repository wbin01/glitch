#!/usr/bin/env python3


class UI(object):
    pass


class Margin(object):
    """..."""
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._QtObject__set_property('property int tMargin', 0)
        self._QtObject__set_property('Layout.topMargin', 'tMargin')

        self._QtObject__set_property('property int rMargin', 0)
        self._QtObject__set_property('Layout.rightMargin', 'rMargin')

        self._QtObject__set_property('property int bMargin', 0)
        self._QtObject__set_property('Layout.bottomMargin', 'bMargin')

        self._QtObject__set_property('property int lMargin', 0)
        self._QtObject__set_property('Layout.leftMargin', 'lMargin')

        self.__image_margin = None

    def __repr__(self) -> str:
        return self.__class__.__name__

    @property
    def margin(self) -> tuple:
        """..."""
        return (
            self._QtObject__property('tMargin'),
            self._QtObject__property('rMargin'),
            self._QtObject__property('bMargin'),
            self._QtObject__property('lMargin'))

    @margin.setter
    def margin(self, margin: int | tuple) -> None:
        # Values
        if not self._QtObject__obj and self._name == 'Image':
            self.__image_margin = margin
            self._render_signal.connect(self.__set_margin)
            return

        top, right, bottom, left = None, None, None, None
        if isinstance(margin, int):
            top, right, bottom, left = margin, margin, margin, margin

        elif isinstance(margin, tuple):
            len_margin = len(margin)
            if len_margin == 1:
                top = margin[0]
            elif len_margin == 2:
                top, right = margin
            elif len_margin == 3:
                top, right, bottom = margin
            else:
                top, right, bottom, left = margin[:4]
        else:
            return

        if top: self._QtObject__set_property('tMargin', top)
        if right: self._QtObject__set_property('rMargin', right)
        if bottom: self._QtObject__set_property('bMargin', bottom)
        if left: self._QtObject__set_property('lMargin', left)

    def __set_margin(self) -> None:
        self.margin = self.__image_margin
