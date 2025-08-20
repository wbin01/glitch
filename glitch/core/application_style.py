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
    class_h = f'[{element.property('className')}{state}]'
    style_h = f'[{element.property('styleClass')}{state}]'
    base_h = f'[{element.property('baseStyle')}{state}]'

    header = style_h if style_h != base_h else class_h
    if header not in style:
        header = class_h if class_h in style else base_h

    # Checkable state
    if element.property('checkable') and element.property('checked'):
        if state == ':inactive':
            header = header.replace(':', ':checked:')
        else:
            # [Element:hover] -> [Element:checked:hover]
            if ':hover' in header:
                header = header.replace(':', ':checked:')
            # [Element] -> [Element:checked]
            elif ':' not in header:
                header = header[:-1] + ':checked]'
            # [Element:clicked] -> [Element:clicked]
            elif ':clicked' in header:
                pass

    # Aply style properties / Only color; margins, size, radius are dinamic
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

    for k, prop in element_properties.items():
        if isinstance(prop, str) and element.property(k):
            if prop in style[header]:
                element.setProperty(k, style_value(style, header, prop))
            elif prop in style[class_h]:
                element.setProperty(k, style_value(style, class_h, prop))
            elif prop in style[base_h]:
                element.setProperty(k, style_value(style, base_h, prop))
        else:
            inner = element.findChild(QtCore.QObject, k)
            if not inner:
                continue

            for k, prop in prop.items():
                if inner.property(k):
                    if prop in style[header]:
                        inner.setProperty(k, style_value(style, header, prop))
                    elif prop in style[class_h]:
                        inner.setProperty(k, style_value(style, class_h, prop))
                    elif prop in style[base_h]:
                        inner.setProperty(k, style_value(style, base_h, prop))
    if canvas:
        inner = element.findChild(QtCore.QObject, 'canvas')
        inner.requestPaint()


def style_value(style: dict, header: str, prop: str) -> str:
    value = style[header][prop]
    # if ',' in value:
    #     return 
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
