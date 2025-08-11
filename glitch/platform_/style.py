#!/usr/bin/env python3


class Style(object):
    """Application style.
    
    Manages style information according to the platform.
    """
    def __init__(self):
        self.style = {
            '[Button]': {
                'background_color': '#333',
                'border_color': '#444',
                'font_color': '#EEE',
                'icon_opacity': 1.0,
                },
            '[Button:inactive]': {
                'background_color': '#222',
                'border_color': '#333',
                'font_color': '#666',
                'icon_opacity': 0.3,
                },
            '[Button:hover]': {
                'background_color': '#383838',
                'border_color': '#883c8cbd',
                'font_color': '#EEE',
                'icon_opacity': 1.0,
                },
            '[Button:clicked]': {
                'background_color': '#333c8cbd',
                'border_color': '#883c8cbd',
                'font_color': '#FFF',
                'icon_opacity': 1.0,
                },
            '[Frame]': {
                'background_color': '#2A2A2A',  # Alt 282828
                'border_color': '#3c8cbd',
                'border_radius': 10,
                },
            '[Frame:inactive]': {
                'background_color': '#222',
                'border_color': '#553c8cbd',
                'border_radius': 10,
                },
            '[Label]': {
                'font_color': '#EEE',
                },
            '[Label:inactive]': {
                'font_color': '#666',
                },
            '[MainFrame]': {
                'background_color': '#2A2A2A',  # Alt 282828
                'border_color': '#333',
                'border_radius': 10,
                },
            '[MainFrame:inactive]': {
                'background_color': '#222',
                'border_color': '#282828',
                'border_radius': 10,
                },
            '[Panel]': {
                'background_color': '#EF222222',
                'border_color': '#222222',
                'border_radius': 10,
                },
            '[Panel:inactive]': {
                'background_color': '#f00',
                'border_color': '#202020',
                'border_radius': 10,
                },
            '[Platform]': {
                'accent_color': '#3c8cbd',
                },
            }
    
    def __str__(self) -> str:
        return "<class 'Style'>"
