class QmlObject:
    def __init__(self, qml_type, object_id=None):
        self.qml_type = qml_type
        self.object_id = object_id
        self.children = []

    def add(self, child):
        self.children.append(child)

    def build(self, tab=0):
        indent = " " * tab
        lines = [f"{indent}{self.qml_type} {{"]
        if self.object_id:
            lines.append(f"{indent}  id: {self.object_id}")

        for child in self.children:
            lines.append(child.build(tab + 2))

        lines.append(f"{indent}}}")
        return "\n".join(lines)

# Subclasses opcionais só para conveniência
class Button(QmlObject):
    def __init__(self, object_id):
        super().__init__('Button', object_id)

class Label(QmlObject):
    def __init__(self, object_id):
        super().__init__('Label', object_id)

class MainObj(QmlObject):
    def __init__(self):
        super().__init__('MainObj', 'mainObj')

# Teste
if __name__ == '__main__':
    root = MainObj()
    button = Button('button')
    label = Label('label')

    label2 = Label('label2')
    label2.add(Label('label3'))

    label.add(button)
    label.add(label2)

    root.add(button)
    root.add(label)

    print(root.build())
