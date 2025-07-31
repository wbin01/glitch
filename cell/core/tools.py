#!/usr/bin/env python3
from PySide6 import QtCore


def change_element_style_state(element, state, style):
    """Adapts the Element's style based on the Frame's state.

    Iterates through the Element's properties and applies a style 
    corresponding to the Frame's current state.
    """
    if element.property('baseClass') != 'Element':
        return

    element_properties = {
        'color': 'font_color',
        'backgroundColor': 'background_color',
        'borderColor': 'border_color',
        'text': {
            'color': 'font_color'},
        'background': {
            'backgroundColor': 'background_color',
            'borderColor': 'border_color'},
        'icon': {
            'opacity': 'icon_opacity'},
        }

    name = f'[{element.property('qmlType')}{state}]'
    for key, value in element_properties.items():
        if isinstance(value, str):
            if element.property(key):
                element.setProperty(key, style[name][value])
        else:
            base_element = element.findChild(QtCore.QObject, key)
            if base_element:
                for key_, value_ in value.items():
                    if base_element.property(key_):
                        base_element.setProperty(
                            key_, style[name][value_])
