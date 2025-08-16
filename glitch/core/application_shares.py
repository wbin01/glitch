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

    header = style_class if style_class != base_style else class_name
    if header not in style:
        header = class_name if class_name in style else base_style

    # Checkable state
    if element.property('checkable') and element.property('checked'):
        if state == ':inactive':
            header = f'[{element.property('className')}:checked:inactive]'
        else:
            if ':hover' in header:
                header = f'[{element.property('className')}:checked:hover]'
            elif ':clicked' in header:
                header = f'[{element.property('className')}:clicked]'
            else:
                header = f'[{element.property('className')}:checked]'

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

    for key, prop in element_properties.items():
        if isinstance(prop, str):
            if element.property(key) and prop in style[header]:
                element.setProperty(key, style_value(style, header, prop))
        else:
            inner = element.findChild(QtCore.QObject, key)
            if not inner:
                continue
            for key, prop in prop.items():
                if inner.property(key) and prop in style[header]:
                    inner.setProperty(key, style_value(style, header, prop))
    if canvas:
        inner = element.findChild(QtCore.QObject, 'canvas')
        inner.requestPaint()


def style_value(style: dict, header: str, prop: str) -> str:
    value = style[header][prop]
    if not value.startswith('['):
        return value

    header, key = value.replace(' ', '').split(']')
    if '#' not in key:
        return style[header + ']'][key]

    key, *alpha = key.split('#')
    alpha = (alpha[0] + 'FF')[:2]

    value = style[header + ']'][key].strip('#')
    len_value  = len(value)

    if len_value == 3:
        value = '#' + alpha + value + value
    elif len_value == 6:
        value = '#' + alpha + value
    else:
        value = '#' + alpha + value[2:]

    return value
