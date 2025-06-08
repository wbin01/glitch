#/usr/bin/env python3
from cell.engine import Application, Handler
from cell.ui import AppFrame 


class View(AppFrame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        
        # button0 = self.add(Button())
        # # button0.object_id = 'button0'
        # label = self.add(Label())

        # box1 = self.add(Box())
        # self.button1 = box1.add(Button())
        # # self.button1.object_id = 'button1'
        # label1 = box1.add(Label())

        # box2 = box1.add(Box())
        # label2 = box2.add(Label())


class Controller(Handler):
    def __init__(self) -> None:
        super().__init__()

        self.load_ui(View())
        
        # print(self.button1)

if __name__ == '__main__':
    app = Application()
    app.handler = Controller()
    app.exec()
