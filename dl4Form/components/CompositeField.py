from components.aux   import *
from components.Field import Field

class CompositeField(Field):
	
	def __init__(self, fields):
		self.fields = fields

	def string_variable_declaration(self):
		var_declaration = ''
		count = 0
		for field in self.fields:
			var_declaration += field.string_variable_declaration()
			count += 1
			if count < len(self.fields):
				var_declaration +=', '
		return var_declaration

	def struct_variable_declaration(self):
		var_declaration = ''
		count = 0
		for field in self.fields:
			var_declaration += field.struct_variable_declaration()
			count += 1
			if count < len(self.fields):
				var_declaration +=', '
		return var_declaration