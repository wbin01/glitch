#!/usr/bin/env python3
from ..base import Box


class Column(Box):
    """Column layout object.

    Organizes elements in stacks like a column.
    """
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.class_id('Column')

    def __str__(self) -> str:
        return "<class 'Column'>"
