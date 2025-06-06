#/usr/bin/env python3
class Layout(object):
	pass

class Widget(object):
	pass

class Layout(Layout):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		self.object_id = object_id
		self.qml_code = None
		self.added_objects = []

	def add(self, obj) -> Layout | Widget:
		self.added_objects.append(obj)
		return obj


class Widget(Widget):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		self.object_id = object_id
		self.qml_code = None


class MainFrame(Layout):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__('mainFrame', *args, **kwargs)
		self.object_id = 'mainFrame'
		self.qml_code = (
			'MainFrame {'
			f'\n    id: mainFrame')
		self.added_objects = []


class Box(Layout):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.qml_code = (
			'\n'
			'\nBox {'
			f'\n    id: {self.object_id}')
		self.added_objects = []


class Button(Widget):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.qml_code = (
			'\n'
			'\nButton {'
			f'\n    id: {self.object_id}')


class Label(Widget):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.qml_code = (
			'\n'
			'\nLabel {'
			f'\n    id: {self.object_id}')


class Model(object):
	# SqLite data model (Optional use)
	pass


class Handler(object):
	def __init__(self) -> None:
		self.ui = ''
		# ...

	def build_ui(self, ui):
		
		for obj in ui.added_objects:
			if isinstance(obj, Layout):
				self.build_ui(obj)

			ui.qml_code += '\n'.join(
				['    ' + x if x else ''
				for x in obj.qml_code.split('\n')]) + '\n    }'

		self.ui = ui.qml_code + '\n}'


class Application(object):
	def __init__(self, controller) -> None:
		self.controller = controller
		# ...

	def exec(self):
		print(self.controller.ui)


if __name__ == '__main__':
	class View(MainFrame):
		def __init__(self, *args, **kwargs) -> None:
			super().__init__(*args, **kwargs)
			
			button = self.add(Button('button'))
			label = self.add(Label('label'))

			box1 = self.add(Box('box1'))
			button1 = box1.add(Button('button1'))
			label1 = box1.add(Label('label1'))

			box2 = box1.add(Box('box2'))
			label2 = box2.add(Label('label2'))


	class Controller(Handler):
		def __init__(self) -> None:
			super().__init__()
			self.build_ui(View())
			# ...


	app = Application(Controller())
	app.exec()
