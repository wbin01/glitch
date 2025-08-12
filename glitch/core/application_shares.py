#!/usr/bin/env python3
from PySide6 import QtCore


@QtCore.Slot()
def change_element_style_state(
        element, state: str, style: dict) -> None:
    """Adapts the Element's style based on the Frame's state.

    Iterates through the Element's properties and applies a style 
    corresponding to the Frame's current state.
    
    :param element: Element object like Button or Label.
    :param state: Frame state like ":inactive".
    :param style: application styles.
    """
    canvas = element.property('className') in ['Panel', 'MainFrame', 'Frame']
    if (element.property('baseClass') != 'Element' and not canvas):
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

    class_name = f'[{element.property('className')}{state}]'
    style_class = f'[{element.property('styleClass')}{state}]'
    base_style = f'[{element.property('baseStyle')}{state}]'

    name = style_class if style_class != base_style else class_name
    if name not in style:
        name = class_name if class_name in style else base_style

    for key, value in element_properties.items():
        if isinstance(value, str):
            if element.property(key) and value in style[name]:
                element.setProperty(key, style[name][value])
            # elif element.property(key) and value in style[base_style]:
            #     element.setProperty(key, style[base_style][value])

        else:
            base_element = element.findChild(QtCore.QObject, key)
            if not base_element:
                continue
            for key_, value_ in value.items():
                if base_element.property(key_) and value_ in style[name]:
                    base_element.setProperty(key_, style[name][value_])
                # elif element.property(key_) and value_ in style[base_style]:
                #     element.setProperty(key_, style[base_style][value_])

    if canvas:
        base_element = element.findChild(QtCore.QObject, 'canvas')
        base_element.requestPaint()
