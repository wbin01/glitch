#!/usr/bin/env python3
from glitch import *


class Window(AppFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


if __name__ == '__main__':
    app = Application(Window)
    app.name = 'Cascão'
    app.exec()
