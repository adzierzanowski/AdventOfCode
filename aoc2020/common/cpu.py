class RepeatedInstructionError(Exception):
  pass

class EndOfCodeError(Exception):
  pass

class CPU:
  def __init__(self, debug_mode=True, stop_after_repetition=True):
    self.acc = 0
    self.pc = 0
    self.already_executed = set()
    self.stop_after_repetition = stop_after_repetition
    self.debug_mode = debug_mode

  def load_code(self, code):
    self.code = code

  def parse(self, instruction):
    opcode, operand = instruction.split(' ')
    return opcode, int(operand)

  def execute(self):
    try:
      opc, ope = self.parse(self.code[self.pc])
    except IndexError:
      raise EndOfCodeError

    if self.debug_mode:
      print(self.pc, opc, ope)

    if self.pc in self.already_executed and self.stop_after_repetition:
      raise RepeatedInstructionError

    self.already_executed.add(self.pc)

    if opc == 'acc':
      self.acc += ope
      self.pc += 1
    elif opc == 'jmp':
      self.pc += ope
    else:
      self.pc += 1
    return True

  def run(self):
    while True:
      self.execute()
