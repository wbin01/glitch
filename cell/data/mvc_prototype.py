#/usr/bin/env python3
class Layout(object):
	pass

class Element(object):
	pass

class Layout(Layout):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		self.__object_id = object_id
		self.__object_code = None
		self.__added_objects = []

	@property
	def object_id(self) -> str:
		"""..."""
		return self.__object_id

	@object_id.setter
	def object_id(self, object_id: str) -> None:
		self.__object_id = object_id

	@property
	def object_code(self) -> str:
		"""..."""
		return self.__object_code

	@object_code.setter
	def object_code(self, object_code: str) -> None:
		self.__object_code = object_code

	@property
	def added_objects(self) -> list:
		"""..."""
		return self.__added_objects

	@added_objects.setter
	def added_objects(self, added_objects: list) -> None:
		self.__added_objects = added_objects

	def add(self, obj) -> Layout | Element:
		"""..."""
		self.__added_objects.append(obj)
		return obj


class Element(Element):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		self.__object_id = object_id
		self.__object_code = None

	@property
	def object_id(self) -> str:
		"""..."""
		return self.__object_id

	@object_id.setter
	def object_id(self, object_id: str) -> None:
		self.__object_id = object_id

	@property
	def object_code(self) -> str:
		"""..."""
		return self.__object_code

	@object_code.setter
	def object_code(self, object_code: str) -> None:
		self.__object_code = object_code


class AppFrame(Layout):
	def __init__(self, *args, **kwargs) -> None:
		super().__init__('appFrame', *args, **kwargs)
		self.object_id = 'appFrame'
		self.object_code = (
			'AppFrame {'
			f'\n    id: appFrame')
		self.added_objects = []


class Box(Layout):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.object_code = (
			'\n'
			'\nBox {'
			f'\n    id: {self.object_id}')
		self.added_objects = []


class Button(Element):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.object_code = (
			'\n'
			'\nButton {'
			f'\n    id: {self.object_id}')


class Label(Element):
	def __init__(self, object_id: str, *args, **kwargs) -> None:
		super().__init__(object_id, *args, **kwargs)
		self.object_id = object_id
		self.object_code = (
			'\n'
			'\nLabel {'
			f'\n    id: {self.object_id}')


class Model(object):
	# SqLite data model (Optional use)
	pass


class Handler(object):
	def __init__(self) -> None:
		self.__qml_code = ''
		# ...

	@property
	def qml_code(self) -> str:
		"""..."""
		return self.__qml_code

	@qml_code.setter
	def qml_code(self, qml_code: str) -> None:
		self.__qml_code = qml_code

	def load_ui(self, qml_code):
		for element in qml_code.added_objects:
			if isinstance(element, Layout):
				self.load_ui(element)

			qml_code.object_code += '\n'.join(
				['    ' + x if x else ''
				for x in element.object_code.split('\n')]) + '\n    }'

		self.__qml_code = qml_code.object_code + '\n}'


class Application(object):
	def __init__(self, controller) -> None:
		self.__controller = controller
		# ...

	def exec(self):
		print(self.__controller.qml_code)


if __name__ == '__main__':
	class View(AppFrame):
		def __init__(self, *args, **kwargs) -> None:
			super().__init__(*args, **kwargs)
			
			button = self.add(Button('button'))
			label = self.add(Label('label'))

			box1 = self.add(Box('box1'))
			button1 = box1.add(Button('button1'))
			label1 = box1.add(Label('label1'))

			box2 = box1.add(Box('box2'))
			label2 = box2.add(Label('label2'))


	class Handles(Handler):
		def __init__(self) -> None:
			super().__init__()
			self.load_ui(View())
			# ...


	app = Application(Handles())
	app.exec()
