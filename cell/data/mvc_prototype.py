#/usr/bin/env python3
class Ui(object):
	# tab = 0
	def __init__(self):
		self.qml_code = (
			'\n'
			'\nMainFrame {'
			'\n    id: mainFrame')
		self.added_objects = []

	def add(self, obj):
		self.added_objects.append(obj)


class Button(Ui):
	def __init__(self, id):
		super().__init__()
		self.qml_code = (
			'\n'
			'\nButton {'
			f'\n    id: {id}')


class Label(Ui):
	def __init__(self, id):
		super().__init__()
		self.qml_code = (
			'\n'
			'\nLabel {'
			f'\n    id: {id}')


class Model(object):
	# SqLite data model (Optional use)
	pass


class Controller(object):
	def __init__(self):
		self.ui = ''
		# Mais codigo de controle abaixo

	def build_ui(self, ui):
		tab = 0
		if ui:
			tab += 4
			for o in ui.added_objects:
				self.build_ui(o)
				ui.qml_code += '\n'.join(
					[(' ' * tab) + x for x in o.qml_code.split('\n')])
			ui.qml_code += '\n}'

		self.ui = ui.qml_code


class Application(object):
	def __init__(self, controller):
		self.controller = controller
		# Mais codigo de integração abaixo

	def exec(self):
		print(self.controller.ui)



if __name__ == '__main__':
	class Ui(Ui):
		def __init__(self):
			super().__init__()
			
			button = Button('button')
			self.add(button)

			label = Label('label')
			self.add(label)

			button2 = Button('button2')
			label.add(button2)

			label2 = Label('label2')
			label.add(label2)

			label3 = Label('label3')
			label2.add(label3)


	class Controller(Controller):
		def __init__(self):
			super().__init__()
			self.build_ui(Ui())
			# Mais códigos de controle daqui para baixo


	app = Application(Controller())
	app.exec()
