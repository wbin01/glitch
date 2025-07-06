#!/usr/bin/env python3
from enum import Enum


class Event(Enum):
    """Event enumeration."""
    NONE = 'NONE'
    ALIGNMENT = 'ALIGNMENT'
    CLOSE = 'CLOSE'
    DELETE = 'DELETE'
    DRAG = 'DRAG'
    DROP = 'DROP'
    ENABLED = 'ENABLED'
    FOCUS_IN = 'FOCUS_IN'
    FOCUS_OUT = 'FOCUS_OUT'
    INSERT = 'INSERT'
    MAIN_PARENT = 'MAIN_PARENT'
    MOUSE_DOUBLE_PRESS = 'MOUSE_DOUBLE_PRESS'
    MOUSE_HOVER_ENTER = 'MOUSE_HOVER_ENTER'
    MOUSE_HOVER_LEAVE = 'MOUSE_HOVER_LEAVE'
    MOUSE_HOVER_MOVE = 'MOUSE_HOVER_MOVE'
    MOUSE_PRESS = 'MOUSE_PRESS'
    MOUSE_RELEASE = 'MOUSE_RELEASE'
    MOUSE_RIGHT_PRESS = 'MOUSE_RIGHT_PRESS'
    MOUSE_WHEEL = 'MOUSE_WHEEL'
    REMOVE = 'REMOVE'
    SIZE = 'SIZE'
    STATE = 'STATE'
    STYLE = 'STYLE'
    STYLE_CLASS = 'STYLE_CLASS'
    STYLE_ID = 'STYLE_ID'
    TITLE = 'TITLE'

    def __str__(self):
        return f'<Event: {id(self)}>'
