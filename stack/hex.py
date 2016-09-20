import math

def to_hex(number, limit=4):
  # Calculo cuantos bits necesito para representar "number" y saco una
  # diferencia con el limite.
  bits = limit - int(math.log(number, 16) + 1)
  # Obtengo el relleno que puede necesitar el numero para llegar al limite.
  fill = '0' * bits
  return '0x' + (fill + '{:x}'.format(number))[-limit:]

def hex_operation(func):
  return lambda hexX, hexY: to_hex(func(hexX, hexY))

def add(hexX, hexY):
  return hex_operation(lambda x,y: x+y)(hexX, hexY)

def sub(hexX, hexY):
  return hex_operation(lambda x,y: x-y)(hexX, hexY)