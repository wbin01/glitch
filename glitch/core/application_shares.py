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
    use_canvas = element.property('className') in ['Panel', 'MainFrame', 'Frame']
    if (element.property('baseClass') != 'Element' and not use_canvas):
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

    name = f'[{element.property('className')}{state}]'
    if name not in style:
        name = f'[{element.property('styleClass')}{state}]'

    for key, value in element_properties.items():
        if isinstance(value, str):
            if element.property(key) and value in style[name]:
                element.setProperty(key, style[name][value])
        else:
            base_element = element.findChild(QtCore.QObject, key)
            if not base_element:
                continue
            for key_, value_ in value.items():
                if base_element.property(key_) and value_ in style[name]:
                    base_element.setProperty(key_, style[name][value_])
                    # if element.property('className') == 'Panel':
                    #     print(value_, style[name][value_])
                    #     element.findChild(
                    #         QtCore.QObject, 'canvas').requestPaint()

    if use_canvas:
        # print(element.property('className'))
        base_element = element.findChild(QtCore.QObject, 'canvas')
        base_element.requestPaint()
