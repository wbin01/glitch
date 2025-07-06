#!/usr/bin/env python3
from enum import Enum


class Orientation(Enum):
    """Orientation enumeration."""
    VERTICAL = 0
    HORIZONTAL = 1

    def __str__(self):
        return f'<Orientation: {id(self)}>'
