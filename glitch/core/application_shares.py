#!/usr/bin/env python3
from PySide6 import QtCore, QtQuick


@QtCore.Slot()
def change_element_style_state(
        element: QtQuick.QQuickItem, state: str, style: dict) -> None:
    """Adapts the Element's style based on the Frame's state.

    Iterates through the Element's properties and applies a style 
    corresponding to the Frame's current state.
    
    :param element: Element object like Button or Label.
    :param state: Frame state like ":inactive".
    :param style: application styles.
    """
    # Mark canvas
    canvas = element.property('className') in ['Panel', 'MainFrame', 'Frame']
    if (element.property('baseClass') != 'Element' and not canvas):
        return

    # Style class
    class_name = f'[{element.property('className')}{state}]'
    style_class = f'[{element.property('styleClass')}{state}]'
    base_style = f'[{element.property('baseStyle')}{state}]'

    name = style_class if style_class != base_style else class_name
    if name not in style:
        name = class_name if class_name in style else base_style

    # Checkable state
    if element.property('checkable') and element.property('checked'):
        if state == ':inactive':
            name = f'[{element.property('className')}:checked:inactive]'
        else:
            if ':hover' in name:
                name = f'[{element.property('className')}:checked:hover]'
            elif ':clicked' in name:
                name = f'[{element.property('className')}:clicked]'
            else:
                name = f'[{element.property('className')}:checked]'

    # Aply style properties
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

    for key, value in element_properties.items():
        if isinstance(value, str):
            if element.property(key) and value in style[name]:
                element.setProperty(key, style_value(style, name, value))
            # elif element.property(key) and value in style[base_style]:
            #     element.setProperty(key, style[base_style][value])
        else:
            inner = element.findChild(QtCore.QObject, key)
            if not inner:
                continue
            for key, value in value.items():
                if inner.property(key) and value in style[name]:
                    inner.setProperty(key, style_value(style, name, value))

    if canvas:
        inner = element.findChild(QtCore.QObject, 'canvas')
        inner.requestPaint()


def style_value(style, name, value) -> str:
    value = style[name][value]
    if not value.startswith('['):
        return value

    name, key = value.split(']')
    key, *alpha = (key + '#').split('#')
    alpha = (alpha[0].strip('*') + 'FF')[:2]

    value = style[name.strip() + ']'][key.strip()].strip('#')
    len_value  = len(value)

    if len_value == 3:
        value = '#' + alpha + value + value
    elif len_value == 6:
        value = '#' + alpha + value
    else:
        value = '#' + alpha + value[2:]

    return value
