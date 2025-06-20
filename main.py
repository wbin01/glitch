#/usr/bin/env python3
from cell.engine import Application, Handler
from cell.ui import AppFrame, Button, Label, ScrollBox


class View(AppFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = self.add(Label('Hello'))
        self.label.margins = None, None, None, 10
        self.button = self.add(Button('Button', 'document-save'))
        self.button.connect(self.on_btn)
        self.button_m = self.add(Button('Button 00', 'document-save'))

        self.scroll = self.add(ScrollBox())
        for item in range(5):
            btn = self.scroll.add(Button(f'Button {item}', 'document-save'))
            btn.connect(self.on_btn)
            setattr(self, f'button_{item}', btn)

        self.scroll.add(Label('Olá'))

    def on_btn(self):
        print(self.label.margins)
        self.label.text = 'HELLO'


class Controller(Handler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.num = 0
        self.button.connect(self.on_button)
        self.button_m.connect(self.on_button)

        for item in range(5):
            btn = getattr(self, f'button_{item}')
            btn.connect(lambda item=item: self.on_num_button(item))
            # btn.margins = 5, 10, 5, 10

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'

    def on_num_button(self, num):
        self.label.text = f'Button press: {num}'


if __name__ == '__main__':
    app = Application(View)
    app.exec()
