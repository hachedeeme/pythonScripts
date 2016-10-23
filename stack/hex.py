import math

def to_hex(number, limit=4):
  # Calculo cuantos bits necesito para representar "number" y saco una
  # diferencia con el limite.
  bits = limit - int(math.log(number, 16) + 1)
  # Obtengo el relleno que puede necesitar el numero para llegar al limite.
  fill = '0' * bits
  return '0x' + (fill + '{:x}'.format(number))[-limit:].upper()

def hex_operation(func):
  return lambda hexX, hexY: to_hex(func(hexX, hexY))

# ============================#
# === Operaciones en Hexa === #
# ============================#
# Estas operaciones pueden recibir tanto numeros decimales 
# como numeros expresados en hexadecimal.
# Retorna el resultado de la operacion expresado en hexa de 
# tipo string.
# Ejemplos: 
# - add(1,2) ------------> 0x0003
# - add(1,0x0003) -------> 0x0004
# - sub(0x00FF,1) -------> 0x00FE
# - sub(0x000A,0x0003) --> 0x0007

def add(hexX, hexY):
  return hex_operation(lambda x,y: x+y)(hexX, hexY)

def sub(hexX, hexY):
  return hex_operation(lambda x,y: x-y)(hexX, hexY)