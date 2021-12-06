from collections import namedtuple
from os import name

Opcode = namedtuple('Opcode', ('opcode', 'mnemonic', 'operand_count'))

class Intcode:
  OPCODES = {
    1: Opcode(1, 'ADD', 3),
    2: Opcode(2, 'MUL', 3),
    3: Opcode(3, 'INP', 1),
    4: Opcode(4, 'OUT', 1),
    5: Opcode(5, 'JNZ', 2),
    6: Opcode(6, 'JZ', 2),
    7: Opcode(7, 'LT', 3),
    8: Opcode(8, 'EQ', 3),
    9: Opcode(9, 'ADJ', 1),
    99: Opcode(99, 'HALT', 0)
  }

  MODE_POS = 0
  MODE_IMM = 1
  MODE_REL = 2

  def __init__(self, debug=False, inputs=None, wfi_mode=False) -> None:
    self.ram = {}
    self.halt = False
    self.wfi_mode = wfi_mode
    self.wait_for_input = False
    self.pc = 0
    self.ic = 0
    self.relbase = 0
    self.debug = debug
    self.initial_inputs = inputs if inputs is not None else []
    self.inputs = self.initial_inputs
    self.input_ptr = 0
    self.outputs = []
    self.initial_program = None
    self.ascii_mode = False

  def set_ascii_mode(self, state):
    self.ascii_mode = state

  def reset(self):
    self.ram = {}
    self.halt = False
    self.pc = 0
    self.ic = 0
    self.inputs = self.initial_inputs
    self.input_ptr = 0
    self.outputs = []
    self.load_program(self.initial_program)

  def dprint(self, *args, color=None, **kwargs):
    if self.debug:
      if color:
        print(f'\x1b[38;5;{color}m' + args[0], *args[1:], '\x1b[0m', **kwargs)
      else:
        print(*args, **kwargs)


  def load_program(self, prog):
    self.initial_program = prog
    for i, val in enumerate(prog):
      self.ram[i] = val

  def read_ram(self, addr):
    return self.ram[addr] if addr in self.ram else (0 if addr >= 0 else 0)

  def read_operand(self, offset, mode=0, dst=False):
    if dst and mode == 0:
      mode = Intcode.MODE_IMM

    ret = 0
    if mode == Intcode.MODE_POS:
      ret = self.read_ram(self.read_ram(self.pc + offset))
    elif mode == Intcode.MODE_IMM:
      ret = self.read_ram(self.pc + offset)
    elif mode == Intcode.MODE_REL:
      if dst:
        ret = self.read_ram(self.pc + offset) + self.relbase
      else:
        ret = self.read_ram(self.read_ram(self.pc + offset) + self.relbase)

    self.dprint(f'Read operand in mode {mode}: {ret}')
    return ret

  def read_opcode(self, addr):
    opc = str(self.read_ram(addr))
    while len(opc) < 5:
      opc = '0' + opc
    modes, opc = opc[:-2], int(opc[-2:])
    opc = Intcode.OPCODES[opc]
    return [int(mode) for mode in modes], opc

  def read_output(self, n=None, clean=True):
    if n:
      out = self.outputs[:n]
      if clean:
        self.outputs = self.outputs[n:]
    else:
      out = self.outputs
      if clean:
        self.outputs = []
    return out

  def execute(self):
    modes, opcode = self.read_opcode(self.pc)

    if self.debug:
      self.dump_state()

    if self.wait_for_input:
      self.dprint('Waiting for input')
      return

    jumped = False

    if opcode.mnemonic == 'ADD':
      a = self.read_operand(1, modes.pop())
      b = self.read_operand(2, modes.pop())
      dst = self.read_operand(3, modes.pop(), dst=True)
      self.dprint(f'[ADD] Store {a} + {b} = {a+b} at {dst}', color=3)
      self.ram[dst] = a + b

    elif opcode.mnemonic == 'MUL':
      a = self.read_operand(1, modes.pop())
      b = self.read_operand(2, modes.pop())
      dst = self.read_operand(3, modes.pop(), dst=True)
      self.dprint(f'[MUL] Store {a} * {b} = {a*b} at {dst}', color=3)
      self.ram[dst] = a * b

    elif opcode.mnemonic == 'INP':
      dst = self.read_operand(1, modes.pop(), dst=True)
      if not (self.inputs and len(self.inputs) > self.input_ptr):
        if self.wfi_mode:
          self.wait_for_input = True
          return
        else:
          inp = input(f'{"ASCII" if self.ascii_mode else "DEC"} >> ')
          if self.ascii_mode:
            if inp == '\\n':
              self.inputs.append(10)
            else:
              for c in inp:
                self.inputs.append(ord(c))
          else:
            self.inputs.append(int(inp))
      self.dprint(f'[INP] Store {self.inputs[self.input_ptr]} at {dst}', color=3)
      self.ram[dst] = self.inputs[self.input_ptr]
      self.input_ptr += 1

    elif opcode.mnemonic == 'OUT':
      out = self.read_operand(1, modes.pop())
      self.dprint(f'[OUT] Output {out}', color=3)
      self.outputs.append(out)

    elif opcode.mnemonic == 'JNZ':
      a = self.read_operand(1, modes.pop())
      dst = self.read_operand(2, modes.pop())
      if a != 0:
        self.dprint(f'[JNZ] Jump to {dst}', color=3)
        self.pc = dst
        jumped = True

    elif opcode.mnemonic == 'JZ':
      a = self.read_operand(1, modes.pop())
      dst = self.read_operand(2, modes.pop())
      if a == 0:
        self.dprint(f'[JZ] Jump to {dst}', color=3)
        self.pc = dst
        jumped = True

    elif opcode.mnemonic == 'LT':
      a = self.read_operand(1, modes.pop())
      b = self.read_operand(2, modes.pop())
      dst = self.read_operand(3, modes.pop(), dst=True)
      self.dprint(f'[LT] Store {1 if a < b else 0} at {dst}', color=3)
      self.ram[dst] = 1 if a < b else 0

    elif opcode.mnemonic == 'EQ':
      a = self.read_operand(1, modes.pop())
      b = self.read_operand(2, modes.pop())
      dst = self.read_operand(3, modes.pop(), dst=True)
      self.dprint(f'[EQ] Store {1 if a == b else 0} at {dst}', color=3)
      self.ram[dst] = 1 if a == b else 0

    elif opcode.mnemonic == 'ADJ':
      diff = self.read_operand(1, modes.pop())
      self.dprint(f'[ADJ] Adjust relative base by {diff}', color=3)
      self.relbase += diff

    elif opcode.mnemonic == 'HALT':
      self.halt = True

    self.ic += 1
    if not jumped:
      self.pc += opcode.operand_count + 1

  def dump_state(self):
    modes, opcode = self.read_opcode(self.pc)
    inputs = [f'\x1b[38;5;1m{x}\x1b[0m' if i == self.input_ptr else f'{x}' for i, x in enumerate(self.inputs)]
    print(f'PC={self.pc} IC={self.ic} OP={opcode.mnemonic} MODES={modes} INPUTS=[{", ".join(inputs)}] INP*={self.input_ptr} OUT={self.outputs} REL={self.relbase}')
    for i in range(self.pc - 10, self.pc+10):
      if i == self.pc:
        print(f'\x1b[38;5;1m{i:8}\x1b[0m', end='')
      else:
        print(f'{i:8}', end='')
    print()
    for i in range(self.pc - 10, self.pc+10):
      print(f'{self.read_ram(i):>8}', end='')
    print()
    print()

  def dump_ram(self):
    i = 0
    ls = []
    while i in self.ram:
      ls.append(self.ram[i])
      i += 1
    return ls

  def feed_inputs(self, *values):
    if self.ascii_mode:
      self.inputs += [10 if v == '\\n' else ord(v) for v in values]
    else:
      self.inputs += values
    self.wait_for_input = False

  def run(self):
    while not self.halt and not self.wait_for_input:
      self.execute()

if __name__ == '__main__':
  cpu = Intcode(debug=True)
  cpu.load_program([109, 2019, 204, -34, 99])
  cpu.ram[1985] = 777
  cpu.run()
  exit()
