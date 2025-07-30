#/usr/bin/env python3
from ..base import Layout


class Column(Layout):
    """Column layout object.

    Organizes elements in stacks like a column.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._element_type = 'Column'

    def __str__(self):
        return "<class 'Column'>"
