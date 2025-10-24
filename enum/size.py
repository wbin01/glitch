#!/usr/bin/env python3
from enum import Enum


class Size(Enum):
    """Size enumeration."""
    AUTO = 'AUTO'
    FILL = 'FILL'
    MAX = 'MAX'
    MIM = 'MIN'

    def __str__(self) -> str:
        return "<class 'Size'>"
