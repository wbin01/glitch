#/usr/bin/env python3
class W1(object):
	tab = 0
	def __init__(self):
		self.text = (
			'\n'
			'\nW1 {'
			'\n  xxx')
		self.adds = []

	def add(self, obj):
		self.adds.append(obj)

	def build(self):
		self.tab += 2
		for o in self.adds:
			o.build()
			tt = [(' ' * self.tab) + x for x in o.text.split('\n')]
			tt = '\n'.join(tt)
			self.text += tt
		self.text += '\n}'


class W2(W1):
	def __init__(self):
		super().__init__()
		self.text = (
			'\n'
			'\nW2 {'
			'\n  xxx')


class W3(W1):
	def __init__(self):
		super().__init__()
		self.text = (
			'\n'
			'\nW3 {'
			'\n  xxx')


if __name__ == '__main__':
	class Ww(W1):
		def __init__(self):
			super().__init__()
			
			w2 = W2()
			self.add(w2)

			w3 = W3()
			self.add(w3)

			ww2 = W2()
			w3.add(ww2)

			ww3 = W3()
			w3.add(ww3)

			www3 = W3()
			ww3.add(www3)


	ww = Ww()
	ww.build()
	print(ww.text)