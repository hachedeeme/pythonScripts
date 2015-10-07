# Create a dl4 Form with simple navigation

from components.CompositeField import CompositeField
from components.TextBox        import TextBox
from components.Label          import Label

from components.aux import *
from Colors import Colors

class DL4Form(object):

	def __init__(self, program_title, x, y):
		self.code = ""
		self.x = x
		self.y = y
		self.fields = []
		self.letter_size      = 5
		self.textBox_heigth   = 6
		self.field_separation = 10
		self.mnemonic_value   = 20
		self.buttons_id       = 100
		self.program_title    = program_title

	# **********************************************************************************
	# CODE GENERATION ******************************************************************
	# **********************************************************************************
	def generate_code(self):
		self.imports()
		self.variable_declaration()
		self.main_screen()
		self.print_ui_components()
		self.goto_first_input()
		self.general_input()
		self.button_pressed_section()
		self.input_section()
		self.add_line('Goto GeneralInput\n')
		self.add_DDBack()
		self.add_InputFill()

	# **********************************************************************************
	# DINAMIC CODE *********************************************************************
	# **********************************************************************************
	def input_section(self):
		components = ''
		last_field = "GeneralInput"
		for field in self.fields:
			components += field.input(last_field)
			if field.declaresConstructor():
				last_field = field.name
		self.add_line(components)

	def declare_field_variables(self):
		struct_vars = '  Dim '
		string_vars = '  Dim '
		count = 0
		for field in self.fields:
			struct_vars += field.struct_variable_declaration()
			string_vars += field.string_variable_declaration()
			count += 1
			if field.declaresConstructor() and count < len(self.fields):
				struct_vars +=', '
				string_vars +=', '

		self.add_line(struct_vars + '\n' + string_vars)

	def fill_components(self):
		components = ''
		for field in self.fields:
			components += '  ' + field.constructor()
			components += ' \ input_y = input_y + field_separation \n'
		self.add_line(components)

	def print_components(self):
		component = ''
		for field in self.fields:
			component = field.print_component()
			if component:
				self.add_line('  ' + component)

	def button_pressed_section(self):
		self.add_jump_separator('ButtonPressedSection')
		self.add_line('  Select Case PressedButton$')
		self.add_line('    Case ""')
		self.add_line('      Goto GeneralInput')
		for field in self.fields:
			component = field.print_case()
			if component:
				self.add_line('    ' + component)
		self.add_line('  End Select')
		self.add_line('')

	def goto_first_input(self):
		self.add_line("Goto " + self.first_input() + '\n')

	# **********************************************************************************
	# STATIC CODE **********************************************************************
	# **********************************************************************************
	def imports(self):
		self.add_line('Declare External Sub DDBack, InputFill, binput_')
		self.add_line('')
		self.add_line('Declare External Sub fill_Label, print_Label')
		self.add_line('')
		self.add_line('Declare External Sub fill_LabelAndTextBox, set_default_or_backup, print_LabelAndTextBox')
		self.add_line('Declare External Sub set_value_backup, set_in_value, set_in_value_and_backup')
		self.add_line('')
		self.add_line('Declare External Sub label, button, printerButton')
		self.add_line('Declare External Function editMode$, addMode$, isEditMode')
		self.add_line('')
		self.add_line('External Lib "lib/ascarui.lib"')
		self.add_line('')
		self.add_line('!===============================================================================')
		self.add_line('Include "includes/uicomponents.inc"')
		self.add_line('!===============================================================================')

	def general_input(self):
		self.add_jump_separator('GeneralInput')
		self.add_line('  Call InputFill(basicInput.,"$",1,7,2, doc$)')
		self.add_line('  Call binput_(basicInput.,"NEW",-1,1,0, PressedButton$)')
		self.add_line('')

	def print_ui_components(self):
		self.add_banner('PRINT UI COMPONENTS')
		self.add_jump_separator('StartUI')
		self.declare_field_variables()
		self.add_line('')
		self.declare_ui_variables()
		self.add_line('')
		self.fill_components()
		self.print_components()
		self.add_line('')

	def declare_ui_variables(self):
		self.add_line('  mode$   = addMode$()')
		self.add_line('  input_x = ' + str(self.x))
		self.add_line('  input_y = ' + str(self.y))
		self.add_line('  letter_size      = ' + str(self.letter_size))
		self.add_line('  textBox_heigth   = ' + str(self.textBox_heigth))
		self.add_line('  field_separation = ' + str(self.field_separation))

	def add_DDBack(self):
		self.add_banner('DDBack')
		self.add_line('External Sub DDBack(title$,_name$,...)')
		self.add_line('  External Lib "lib/colors.lib"')
		self.add_line('  Declare External Function LAB01_Title$')
		self.add_line('  Declare External Function LAB07_Borders$')
		self.add_line('  Declare External Function LAB09_ResetPen$')
		self.add_line('  Declare External Function LAB10_Time$')
		self.add_line('  Declare External Function TopOfWindow_b')
		self.add_line('  Dim %1,_x,scale')
		self.add_line('  Dim COLTITLE$[100],COLBORD$[100],COLRESETP$[100],COLTIME$[100]')
		self.add_line('  Try Enter yOffset Else Dim yOffset')
		self.add_line('  !')
		self.add_line('  COLTITLE$ = LAB01_Title$()')
		self.add_line('  COLBORD$ = LAB07_Borders$()')
		self.add_line('  COLRESETP$ = LAB09_ResetPen$()')
		self.add_line('  COLTIME$ = LAB10_Time$()')
		self.add_line('  !')
		self.add_line('  x = Int((80 - Len(RTrim$(LTrim$(title$)))) / 2)')
		self.add_line("  Print 'CS'")
		self.add_line('  If _x < 3 Let _x = 3')
		self.add_line('  Print COLBORD$')
		self.add_line('  Print PChr$(5,2,12,Msc(33)-22,Msc(34)-30,"");' + "'WCGROUP'")
		self.add_line('  Print COLRESETP$;')
		self.add_line('  xx = TopOfWindow_b(title$,_name$,yOffset,10)')
		self.add_line('  Print COLTIME$;')
		self.add_line('End Sub\n')


	def add_InputFill(self):
		self.add_banner('input fill structure')
		self.add_line('External Sub InputFill(inpuStruct. as inchk, type$, length, x,y, doc$)')
		self.add_line('  inpuStruct.ti$ = type$ \ inpuStruct.valu$ = ""')
		self.add_line('  inpuStruct.ilen = length')
		self.add_line('  inpuStruct.opt$ = "UP" + "GR" + Str$(10) \ inpuStruct.doc$ = doc$')
		self.add_line('  inpuStruct.xco = x \ inpuStruct.yco = y')
		self.add_line('End Sub\n')

	def variable_declaration(self):
		self.add_line('Dim mode$[4]')
		self.add_line('')
		self.add_line('Dim basicInput. As inchk')
		self.add_line('Dim PressedButton$[40]')
		self.add_line('')

	def main_screen(self):
		self.add_jump_separator('MainScreen')
		self.add_line('  ! Main Screen configuration')
		self.add_line('  Window On')
		self.add_line('  Window Clear')
		self.add_line("  Print 'XX'")
		self.add_line("  Print '90,29WALTSIZE';")
		self.add_line('  Window Open @0,0; To @Msc(40) + 1,Msc(41);')
		self.add_line('')
		self.add_line("  Print PChr$(10);'GRIDFONT';")
		self.add_line('  Print PChr$("Arial Mono for dL4")' + ";'FONTFACE';")
		self.add_line("  Print PChr$(5);'FONTSIZE';")
		self.add_line("  Print 'EBOLD'")
		self.add_line("  Print 'WCSETFONT'")
		self.add_line('')
		self.add_DDBack_call()
		self.add_line('  ! Add BACK, NEXT and QUIT buttons.')
		self.add_line('  Call GuiHeaderBtns_b("BACK%NEXT%QUI2%","111",2,42,10,1)')
		self.add_line('  Print ;COLDATA$;@20,22;"            "')
		self.add_line('')

	def add_DDBack_call(self):
		self.add_line('  Call DDBack("' + self.program_title.upper() + '",Msc$(4))')

	# **********************************************************************************
	# FUNCTIONS ************************************************************************
	# **********************************************************************************
	def first_input(self):
		first_input = ''
		for field in self.fields:
			if field.isInput():
				return field.name
		return first_input

	def add_TextBox(self, field_name, label_text, size, default_value, color):
		self.add_field(TextBox(self.get_button_id(), field_name, label_text, size, color, self.get_mnemonic_value(), default_value))
		
	def add_Label(self, field_name, label_text, color):
		self.add_field(Label(field_name, label_text, color))

	def add_banner(self, banner_title):
		self.add_line('!===============================================================================')
		self.add_line('! ' + banner_title.upper())
		self.add_line('!===============================================================================')

	def add_jump_separator(self, name):
		self.add_line(jump_separator(name))

	def add_line(self, a_code_line):
		self.code += ("\n" + a_code_line)

	def get_button_id(self):
		self.buttons_id += 1
		return self.buttons_id

	def get_mnemonic_value(self):
		self.mnemonic_value += 1
		return self.mnemonic_value

	def add_field(self, field):
		self.fields.append(field)