#/usr/bin/env python3
from cell.engine import Application, Handler
from cell.ui import Ui, Button


class View(Ui):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.button = self.add(Button('Press'))
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
        self.button.connect(self.on_button)

    def on_button(self):
        self.button.text = 'Apertou miseravi!'

if __name__ == '__main__':
    app = Application(View())
    app.handler = Controller(app.gui, app.ui)
    app.exec()
