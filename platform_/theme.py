#!/usr/bin/env python3
import os
import platform


class Theme(object):
    """..."""
    def __init__(self) -> None:
        self.__accent_color = None
        self.__theme = None

    def __repr__(self) -> str:
        return self.__class__.__name__
    
    @property
    def accent_color(self) -> str:
        """..."""
        pass

    @accent_color.setter
    def accent_color(self, accent_color: str) -> None:
        pass

    @property
    def theme(self) -> str:
        """..."""
        pass

    @theme.setter
    def theme(self, theme: str) -> None:
        pass
