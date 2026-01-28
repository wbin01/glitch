#!/usr/bin/env python3
from glitch import *


class Window(AppFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.over = self.add(Context(modal=True))
        # self.over.width, self.over.height = 100, 30
        # self.margin = 10,

        self._right_pressed_signal.connect(self.over_open)

        self.panel = self.add(Panel())
        self.modal = self.add(Modal())
        self.modal.add(Label('Modal'))
        # self.modal.width, self.modal.height = 300, 100
        # self.modal.margin = 10


        self.tbl = self.header.add(ToolButton('document-open'))
        self.tbl._clicked_signal.connect(lambda: self.panel.open(Anim.LEFT))
        
        self.tbr = self.header.add(ToolButton('document-open'), right=True)
        self.tbr._clicked_signal.connect(lambda: self.panel.open(Anim.RIGHT))

        self.container = self.add(Column())
        self.container.margin = 2
        
        self.btnt1 = self.container.add(Button('TOP'))
        self.btnt1._clicked_signal.connect(lambda: self.modal_open(Anim.TOP))

        self.over = self.container.add(Context(modal=False, x=None, y=None))
        self.over_col = self.over.add(Column())
        # self.over_col.align = Align.TOP

        self.btn_over = self.over_col.add(Button('Button over'))
        self.btn_over1 = self.over_col.add(Button('Button over'))
        self.btn_over2 = self.over_col.add(Button('Button over'))

        self.btnb1 = self.container.add(Button('BOTTOM'))
        self.btnb1._clicked_signal.connect(lambda: self.modal_open(Anim.BOTTOM))

        self.btnl1 = self.container.add(Button('LEFT'))
        self.btnl1._clicked_signal.connect(lambda: self.modal_open(Anim.LEFT))

        self.btnr1 = self.container.add(Button('RIGHT'))
        self.btnr1._clicked_signal.connect(lambda: self.modal_open(Anim.RIGHT))

        self.btnc = self.container.add(Button('CENTER'))
        self.btnc._clicked_signal.connect(lambda: self.modal_open(Anim.CENTER))

    def modal_open(self, anim):
        self.modal.reset()
        if anim == Anim.TOP:
            # self.modal.width = self.width[0] - 50
            # self.modal.height = self.height[0] - 50
            # self.modal.static = True
            pass
        elif anim == Anim.BOTTOM:
            pass
        elif anim == Anim.LEFT:
            pass
        elif anim == Anim.RIGHT:
            pass
        elif anim == Anim.CENTER:
            pass
        self.modal.open(anim)

    def over_open(self, anim=Anim.TOP):
        # self.over.width, self.over.height = self.container.width[0], 50
        # self.over.height = 50
        # self.over.width = 50
        if anim == Anim.TOP:
            pass
        elif anim == Anim.BOTTOM:
            pass
        elif anim == Anim.LEFT:
            pass
        elif anim == Anim.RIGHT:
            pass
        elif anim == Anim.CENTER:
            pass

        if not self.over.visible:
            self.over.open(anim)
        else:
            self.over.close()
        self.modal.close()

if __name__ == '__main__':
    app = Application(Window)
    # app.name = 'Cascão'
    app.exec()
