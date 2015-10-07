from components.CompositeField import CompositeField
from components.TextBox        import TextBox
from components.Label          import Label
from dl4_forms                 import DL4Form

from components.aux import *
from Colors import Colors

dl4_file = open('dl4_form.bas', 'w')


form = DL4Form('Email Addres Book Maintenance', x=40, y=50)

form.add_TextBox('Company',  '0) Company   :  ', 50, "Default Value", Colors.COLLABEL)
form.add_Label('', '', Colors.COLLABEL)
form.add_TextBox('Contact1', '1) Contact #1:  ', 30, "Default Value", Colors.COLLABEL)
form.add_TextBox('Email1'  , '   Email #1  :  ', 50, "Default Value", Colors.COLLABEL)
form.add_Label('', '', Colors.COLLABEL)
form.add_TextBox('Contact2', '2) Contact #2:  ', 30, "Default Value", Colors.COLLABEL)
form.add_TextBox('Email2'  , '   Email #2  :  ', 50, "Default Value", Colors.COLLABEL)
form.add_Label('', '', Colors.COLLABEL)
form.add_TextBox('Contact3', '3) Contact #3:  ', 30, "Default Value", Colors.COLLABEL)
form.add_TextBox('Email3'  , '   Email #3  :  ', 50, "Default Value", Colors.COLLABEL)
form.add_Label('', '', Colors.COLLABEL)
form.add_TextBox('Contact4', '4) Contact #4:  ', 30, "Default Value", Colors.COLLABEL)
form.add_TextBox('Email4'  , '   Email #4  :  ', 50, "Default Value", Colors.COLLABEL)
form.add_Label('', '', Colors.COLLABEL)
form.add_TextBox('Contact5', '5) Contact #5:  ', 30, "Default Value", Colors.COLLABEL)
form.add_TextBox('Email5'  , '   Email #5  :  ', 50, "Default Value", Colors.COLLABEL)

form.generate_code()
#form.declare_field_variables()

dl4_file.write(form.code)
dl4_file.close()