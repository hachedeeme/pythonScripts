from components.aux   import *
from components.Field import Field

class TextBox(Field):

	def __init__(self, id, name, label_text, size, color, mnemonic_value, default_value):
		super().__init__(name, label_text, color)
		self.id   = id
		self.size = size
		self.default_value  = default_value
		self.mnemonic_value = mnemonic_value

	def struct_variable_declaration(self):
		return first_to_lowercase(self.name) + '. As LabelAndTextBox'

	def string_variable_declaration(self):
		return first_to_lowercase(self.name) + "$[" + str(self.size) + "]"

	def print_component(self):
		return "Call print_LabelAndTextBox(" + first_to_lowercase(self.name) + ".)"

	def constructor(self):
		res  = "Call fill_LabelAndTextBox(" + first_to_lowercase(self.name) + '., "' + self.label_text + '", '
		res += self.color.value + ", input_x, input_y, letter_size, " + str(self.id) + ', ' + first_to_lowercase(self.name) +  '$, textBox_heigth, '
		res += str(self.size) + ", 'F" + str(self.mnemonic_value) + "')"
		return res

	def print_case(self):
		return 'Case "' + str(self.mnemonic_value) + '"' + '\n      Goto ' + self.name

	def input(self, last_field):
		field_name = first_to_lowercase(self.name)
		input = jump_separator(self.name)
		input += '\nCall InputFill(basicInput.,"$", ' + field_name + '.t_box.length, ' + field_name + '.t_box.x/10, ' + field_name + '.t_box.y/10, doc$) \n'
		input += 'basicInput.mask$ = "' + ('*' * self.size) + '"\n\n'
		input += 'Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)\n\n'
		input += 'If basicInput.valu$ = "" and PressedButton$ = ""\n'
		input += '  Call set_default_or_backup(' + field_name + '., "' + self.default_value + '")\n'
		input += 'Else If PressedButton$ <> ""\n'
		input += '  If basicInput.valu$ <> "" Call set_in_value_and_backup(' + field_name + '., basicInput.valu$)\n'
		input += '  Call print_LabelAndTextBox(' + field_name + '.)\n'
		input += '  mode$ = editMode$()\n'
		input += '  Goto ButtonPressedSection\n'
		input += 'Else If basicInput.valu$ = "*"\n'
		input += '  Call print_LabelAndTextBox(' + field_name + '.)\n'
		input += '  If isEditMode(mode$) Goto GeneralInput\n'
		input += '  Goto ' + last_field + '\n'
		input += 'Else\n'
		input += '  Call set_in_value_and_backup(' + field_name + '., basicInput.valu$)\n'
		input += 'End If\n\n'
		input += 'Call print_LabelAndTextBox(' + field_name + '.)\n\n'
		input += 'If isEditMode(mode$) Goto GeneralInput\n\n'
		return input

	def declaresConstructor(self):
		return True

	def isInput(self):
		return True

#!EmployersFederalId: !=============================================================
#!  Call InputFill(basicInput.,"$", employersFederalId.t_box.length, employersFederalId.t_box.x/10, employersFederalId.t_box.y/10, doc$)
#!  basicInput.mask$ = "********************"
#!
#!  Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)
#!
#!  If basicInput.valu$ = "" and PressedButton$ = ""
#!    Call set_default_or_backup(employersFederalId., "")
#!  Else If PressedButton$ <> ""
#!    If basicInput.valu$ <> "" Call set_in_value_and_backup(employersFederalId., basicInput.valu$)
#!    Call print_LabelAndTextBox(employersFederalId.)
#!    mode$ = editMode$()
#!    Goto ButtonPressedSection
#!  Else If basicInput.valu$ = "*"
#!    Call print_LabelAndTextBox(employersFederalId.)
#!    Goto GeneralInput
#!  Else
#!    Call set_in_value_and_backup(employersFederalId., basicInput.valu$)
#!  End If
#!
#!  Call print_LabelAndTextBox(employersFederalId.)
#!
#!  If isEditMode(mode$) Goto GeneralInput