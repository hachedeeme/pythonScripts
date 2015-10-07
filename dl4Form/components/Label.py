from components.Field import Field

class Label(Field):

	def constructor(self):
		return 'Call label(input_x, input_y, "' + self.label_text + '", ' + self.color.value + ')'