from components.aux import *

class Field():
	def __init__(self, name, label_text, color):
		self.name = name
		self.label_text = label_text
		self.color      = color

	def string_variable_declaration(self):
		return ''

	def struct_variable_declaration(self):
		return ''

	def print_component(self):
		return ''

	def constructor(self):
		return ''

	def print_case(self):
		return ''

	def input(self, last_field):
		return ''

	def declaresConstructor(self):
		return False

	def isInput(self):
		return False
