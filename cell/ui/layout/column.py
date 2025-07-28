#/usr/bin/env python3
from ..base import Layout


class Column(Layout):
    """Column layout object.

    Organizes elements in stacks like a column.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
