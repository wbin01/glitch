#/usr/bin/env python3
from .layout import Layout
from ..enum.orientation import Orientation


class Row(Layout):
    """..."""
    def __init__(
            self, orientation: Orientation = Orientation.HORIZONTAL,
            *args, **kwargs) -> None:
        """..."""
        super().__init__(orientation=orientation, *args, **kwargs)
