
Declare External Sub DDBack, InputFill, binput_

Declare External Sub fill_Label, print_Label

Declare External Sub fill_LabelAndTextBox, set_default_or_backup, print_LabelAndTextBox
Declare External Sub set_value_backup, set_in_value, set_in_value_and_backup

Declare External Sub label, button, printerButton
Declare External Function editMode$, addMode$, isEditMode

External Lib "lib/ascarui.lib"

!===============================================================================
Include "includes/uicomponents.inc"
!===============================================================================
Dim mode$[4]

Dim basicInput. As inchk
Dim PressedButton$[40]

MainScreen: !===================================================================
  ! Main Screen configuration
  Window On
  Window Clear
  Print 'XX'
  Print '90,29WALTSIZE';
  Window Open @0,0; To @Msc(40) + 1,Msc(41);

  Print PChr$(10);'GRIDFONT';
  Print PChr$("Arial Mono for dL4");'FONTFACE';
  Print PChr$(5);'FONTSIZE';
  Print 'EBOLD'
  Print 'WCSETFONT'

  Call DDBack("EMAIL ADDRES BOOK MAINTENANCE",Msc$(4))
  ! Add BACK, NEXT and QUIT buttons.
  Call GuiHeaderBtns_b("BACK%NEXT%QUI2%","111",2,42,10,1)
  Print ;COLDATA$;@20,22;"            "

!===============================================================================
! PRINT UI COMPONENTS
!===============================================================================
StartUI: !======================================================================
  Dim company. As LabelAndTextBox, contact1. As LabelAndTextBox, email1. As LabelAndTextBox, contact2. As LabelAndTextBox, email2. As LabelAndTextBox, contact3. As LabelAndTextBox, email3. As LabelAndTextBox, contact4. As LabelAndTextBox, email4. As LabelAndTextBox, contact5. As LabelAndTextBox, email5. As LabelAndTextBox
  Dim company$[50], contact1$[30], email1$[50], contact2$[30], email2$[50], contact3$[30], email3$[50], contact4$[30], email4$[50], contact5$[30], email5$[50]

  mode$   = addMode$()
  input_x = 40
  input_y = 50
  letter_size      = 5
  textBox_heigth   = 6
  field_separation = 10

  Call fill_LabelAndTextBox(company., "0) Company   :  ", COLLABEL$, input_x, input_y, letter_size, 101, company$, textBox_heigth, 50, 'F21') \ input_y = input_y + field_separation 
  Call label(input_x, input_y, "", COLLABEL$) \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(contact1., "1) Contact #1:  ", COLLABEL$, input_x, input_y, letter_size, 102, contact1$, textBox_heigth, 30, 'F22') \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(email1., "   Email #1  :  ", COLLABEL$, input_x, input_y, letter_size, 103, email1$, textBox_heigth, 50, 'F23') \ input_y = input_y + field_separation 
  Call label(input_x, input_y, "", COLLABEL$) \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(contact2., "2) Contact #2:  ", COLLABEL$, input_x, input_y, letter_size, 104, contact2$, textBox_heigth, 30, 'F24') \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(email2., "   Email #2  :  ", COLLABEL$, input_x, input_y, letter_size, 105, email2$, textBox_heigth, 50, 'F25') \ input_y = input_y + field_separation 
  Call label(input_x, input_y, "", COLLABEL$) \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(contact3., "3) Contact #3:  ", COLLABEL$, input_x, input_y, letter_size, 106, contact3$, textBox_heigth, 30, 'F26') \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(email3., "   Email #3  :  ", COLLABEL$, input_x, input_y, letter_size, 107, email3$, textBox_heigth, 50, 'F27') \ input_y = input_y + field_separation 
  Call label(input_x, input_y, "", COLLABEL$) \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(contact4., "4) Contact #4:  ", COLLABEL$, input_x, input_y, letter_size, 108, contact4$, textBox_heigth, 30, 'F28') \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(email4., "   Email #4  :  ", COLLABEL$, input_x, input_y, letter_size, 109, email4$, textBox_heigth, 50, 'F29') \ input_y = input_y + field_separation 
  Call label(input_x, input_y, "", COLLABEL$) \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(contact5., "5) Contact #5:  ", COLLABEL$, input_x, input_y, letter_size, 110, contact5$, textBox_heigth, 30, 'F30') \ input_y = input_y + field_separation 
  Call fill_LabelAndTextBox(email5., "   Email #5  :  ", COLLABEL$, input_x, input_y, letter_size, 111, email5$, textBox_heigth, 50, 'F31') \ input_y = input_y + field_separation 

  Call print_LabelAndTextBox(company.)
  Call print_LabelAndTextBox(contact1.)
  Call print_LabelAndTextBox(email1.)
  Call print_LabelAndTextBox(contact2.)
  Call print_LabelAndTextBox(email2.)
  Call print_LabelAndTextBox(contact3.)
  Call print_LabelAndTextBox(email3.)
  Call print_LabelAndTextBox(contact4.)
  Call print_LabelAndTextBox(email4.)
  Call print_LabelAndTextBox(contact5.)
  Call print_LabelAndTextBox(email5.)

Goto Company

GeneralInput: !=================================================================
  Call InputFill(basicInput.,"$",1,7,2, doc$)
  Call binput_(basicInput.,"NEW",-1,1,0, PressedButton$)

ButtonPressedSection: !=========================================================
  Select Case PressedButton$
    Case ""
      Goto GeneralInput
    Case "21"
      Goto Company
    Case "22"
      Goto Contact1
    Case "23"
      Goto Email1
    Case "24"
      Goto Contact2
    Case "25"
      Goto Email2
    Case "26"
      Goto Contact3
    Case "27"
      Goto Email3
    Case "28"
      Goto Contact4
    Case "29"
      Goto Email4
    Case "30"
      Goto Contact5
    Case "31"
      Goto Email5
  End Select

Company: !======================================================================
Call InputFill(basicInput.,"$", company.t_box.length, company.t_box.x/10, company.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(company., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(company., basicInput.valu$)
  Call print_LabelAndTextBox(company.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(company.)
  If isEditMode(mode$) Goto GeneralInput
  Goto GeneralInput
Else
  Call set_in_value_and_backup(company., basicInput.valu$)
End If

Call print_LabelAndTextBox(company.)

If isEditMode(mode$) Goto GeneralInput

Contact1: !=====================================================================
Call InputFill(basicInput.,"$", contact1.t_box.length, contact1.t_box.x/10, contact1.t_box.y/10, doc$) 
basicInput.mask$ = "******************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(contact1., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(contact1., basicInput.valu$)
  Call print_LabelAndTextBox(contact1.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(contact1.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Company
Else
  Call set_in_value_and_backup(contact1., basicInput.valu$)
End If

Call print_LabelAndTextBox(contact1.)

If isEditMode(mode$) Goto GeneralInput

Email1: !=======================================================================
Call InputFill(basicInput.,"$", email1.t_box.length, email1.t_box.x/10, email1.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(email1., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(email1., basicInput.valu$)
  Call print_LabelAndTextBox(email1.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(email1.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Contact1
Else
  Call set_in_value_and_backup(email1., basicInput.valu$)
End If

Call print_LabelAndTextBox(email1.)

If isEditMode(mode$) Goto GeneralInput

Contact2: !=====================================================================
Call InputFill(basicInput.,"$", contact2.t_box.length, contact2.t_box.x/10, contact2.t_box.y/10, doc$) 
basicInput.mask$ = "******************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(contact2., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(contact2., basicInput.valu$)
  Call print_LabelAndTextBox(contact2.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(contact2.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Email1
Else
  Call set_in_value_and_backup(contact2., basicInput.valu$)
End If

Call print_LabelAndTextBox(contact2.)

If isEditMode(mode$) Goto GeneralInput

Email2: !=======================================================================
Call InputFill(basicInput.,"$", email2.t_box.length, email2.t_box.x/10, email2.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(email2., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(email2., basicInput.valu$)
  Call print_LabelAndTextBox(email2.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(email2.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Contact2
Else
  Call set_in_value_and_backup(email2., basicInput.valu$)
End If

Call print_LabelAndTextBox(email2.)

If isEditMode(mode$) Goto GeneralInput

Contact3: !=====================================================================
Call InputFill(basicInput.,"$", contact3.t_box.length, contact3.t_box.x/10, contact3.t_box.y/10, doc$) 
basicInput.mask$ = "******************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(contact3., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(contact3., basicInput.valu$)
  Call print_LabelAndTextBox(contact3.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(contact3.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Email2
Else
  Call set_in_value_and_backup(contact3., basicInput.valu$)
End If

Call print_LabelAndTextBox(contact3.)

If isEditMode(mode$) Goto GeneralInput

Email3: !=======================================================================
Call InputFill(basicInput.,"$", email3.t_box.length, email3.t_box.x/10, email3.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(email3., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(email3., basicInput.valu$)
  Call print_LabelAndTextBox(email3.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(email3.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Contact3
Else
  Call set_in_value_and_backup(email3., basicInput.valu$)
End If

Call print_LabelAndTextBox(email3.)

If isEditMode(mode$) Goto GeneralInput

Contact4: !=====================================================================
Call InputFill(basicInput.,"$", contact4.t_box.length, contact4.t_box.x/10, contact4.t_box.y/10, doc$) 
basicInput.mask$ = "******************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(contact4., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(contact4., basicInput.valu$)
  Call print_LabelAndTextBox(contact4.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(contact4.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Email3
Else
  Call set_in_value_and_backup(contact4., basicInput.valu$)
End If

Call print_LabelAndTextBox(contact4.)

If isEditMode(mode$) Goto GeneralInput

Email4: !=======================================================================
Call InputFill(basicInput.,"$", email4.t_box.length, email4.t_box.x/10, email4.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(email4., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(email4., basicInput.valu$)
  Call print_LabelAndTextBox(email4.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(email4.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Contact4
Else
  Call set_in_value_and_backup(email4., basicInput.valu$)
End If

Call print_LabelAndTextBox(email4.)

If isEditMode(mode$) Goto GeneralInput

Contact5: !=====================================================================
Call InputFill(basicInput.,"$", contact5.t_box.length, contact5.t_box.x/10, contact5.t_box.y/10, doc$) 
basicInput.mask$ = "******************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(contact5., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(contact5., basicInput.valu$)
  Call print_LabelAndTextBox(contact5.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(contact5.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Email4
Else
  Call set_in_value_and_backup(contact5., basicInput.valu$)
End If

Call print_LabelAndTextBox(contact5.)

If isEditMode(mode$) Goto GeneralInput

Email5: !=======================================================================
Call InputFill(basicInput.,"$", email5.t_box.length, email5.t_box.x/10, email5.t_box.y/10, doc$) 
basicInput.mask$ = "**************************************************"

Call binput_(basicInput.,"NEW",-1,0,0, PressedButton$)

If basicInput.valu$ = "" and PressedButton$ = ""
  Call set_default_or_backup(email5., "Default Value")
Else If PressedButton$ <> ""
  If basicInput.valu$ <> "" Call set_in_value_and_backup(email5., basicInput.valu$)
  Call print_LabelAndTextBox(email5.)
  mode$ = editMode$()
  Goto ButtonPressedSection
Else If basicInput.valu$ = "*"
  Call print_LabelAndTextBox(email5.)
  If isEditMode(mode$) Goto GeneralInput
  Goto Contact5
Else
  Call set_in_value_and_backup(email5., basicInput.valu$)
End If

Call print_LabelAndTextBox(email5.)

If isEditMode(mode$) Goto GeneralInput


Goto GeneralInput

!===============================================================================
! DDBACK
!===============================================================================
External Sub DDBack(title$,_name$,...)
  External Lib "lib/colors.lib"
  Declare External Function LAB01_Title$
  Declare External Function LAB07_Borders$
  Declare External Function LAB09_ResetPen$
  Declare External Function LAB10_Time$
  Declare External Function TopOfWindow_b
  Dim %1,_x,scale
  Dim COLTITLE$[100],COLBORD$[100],COLRESETP$[100],COLTIME$[100]
  Try Enter yOffset Else Dim yOffset
  !
  COLTITLE$ = LAB01_Title$()
  COLBORD$ = LAB07_Borders$()
  COLRESETP$ = LAB09_ResetPen$()
  COLTIME$ = LAB10_Time$()
  !
  x = Int((80 - Len(RTrim$(LTrim$(title$)))) / 2)
  Print 'CS'
  If _x < 3 Let _x = 3
  Print COLBORD$
  Print PChr$(5,2,12,Msc(33)-22,Msc(34)-30,"");'WCGROUP'
  Print COLRESETP$;
  xx = TopOfWindow_b(title$,_name$,yOffset,10)
  Print COLTIME$;
End Sub

!===============================================================================
! INPUT FILL STRUCTURE
!===============================================================================
External Sub InputFill(inpuStruct. as inchk, type$, length, x,y, doc$)
  inpuStruct.ti$ = type$ \ inpuStruct.valu$ = ""
  inpuStruct.ilen = length
  inpuStruct.opt$ = "UP" + "GR" + Str$(10) \ inpuStruct.doc$ = doc$
  inpuStruct.xco = x \ inpuStruct.yco = y
End Sub
