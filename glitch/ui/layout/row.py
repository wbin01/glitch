#!/usr/bin/env python3
from ..base import MarginsMixin, Layout
from ...enum.orientation import Orientation


class Row(MarginsMixin, Layout):
    """Row layout object.

    Organizes elements side by side like a row.
    """
    def __init__(
            self, orientation: Orientation = Orientation.HORIZONTAL,
            *args, **kwargs) -> None:
        super().__init__(orientation=orientation, *args, **kwargs)
        self.class_id('Row')

    def __str__(self) -> str:
        return "<class 'Row'>"
