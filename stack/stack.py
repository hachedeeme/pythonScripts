import string

def hex_sintax(hex_string):
  hex_digits = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f'] 
  count = True
  for char in hex_string.lower():
    count = count and char in hex_digits
  return count

# ========================================================================
class DirMode():
  def __init__(self, source):
    self.source = source

  def validate(self):
    raise Exception("ERROR GROSO - Este es un metodo abstracto. ")

# ========================================================================
class Direct(DirMode):
  def __init__(self, source):
    DirMode.__init__(self, source)

  def validate(self):
    return '[' in self.source and ']' in self.source and len(self.source) == 8

# ========================================================================
class Register(DirMode):
  def __init__(self, source):
    DirMode.__init__(self, source)

  def validate(self):
    count = False
    for n in range(0,8):
      count = count or str(n) in self.source 
    return 'R' in self.source[:1] and len(self.source) == 2 and count

# ========================================================================
class Immediate(DirMode):
  def __init__(self, source):
    DirMode.__init__(self, source)

  def validate(self):
    return len(self.source) == 6 and '0x' == self.source[:2] and hex_sintax(self.source[-4:])

# ========================================================================
class BinOp():
  def __init__(self, destination, origin):
    self.destination = destination
    self.origin      = origin



print Direct("[0xasas]").validate()
print Register("R0").validate()
print Immediate("0xFFFF").validate()
