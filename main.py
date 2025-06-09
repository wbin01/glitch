#/usr/bin/env python3
from cell.engine import Application, Handler
from cell.ui import Ui, Button, Label


class View(Ui):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.label = self.add(Label('Hello'))
        self.button = self.add(Button('Button', 'document-save'))

        for item in range(5):
            btn = self.add(Button(f'Button {item}', 'document-save'))
            setattr(self, f'button_{item}', btn)
            
        # label = self.add(Label())

        # box1 = self.add(Box())
        # self.button1 = box1.add(Button())
        # # self.button1.object_id = 'button1'
        # label1 = box1.add(Label())

        # box2 = box1.add(Box())
        # label2 = box2.add(Label())


class Controller(Handler):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.num = 0

        self.button.connect(self.on_button)
        self.label.margins = 50, 20, 50, 20

        for item in range(5):
            btn = getattr(self, f'button_{item}')
            btn.connect(lambda item=item: self.on_num_button(item))

    def on_button(self):
        self.num += 1
        self.label.text = f'Button press: {self.num}'
        print(self.button.margins)
        self.button.margins = None, 100, None, 100

    def on_num_button(self, num):
        # self.num += 1
        self.label.text = f'Button press: {num}'

if __name__ == '__main__':
    app = Application(View())
    app.handler = Controller(app.gui, app.ui)
    app.exec()
