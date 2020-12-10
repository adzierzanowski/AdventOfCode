from common.cpu import CPU, EndOfCodeError, RepeatedInstructionError
from helpers import readlines, rpath, tpath


def part1(data):
  cpu = CPU(debug_mode=False)
  cpu.load_code(data)

  try:
    cpu.run()
  except RepeatedInstructionError:
    pass

  return cpu.acc

def part2(data):
  for i, line in enumerate(data):
    newcode = data[:]

    if 'jmp' in line:
      newcode[i] = newcode[i].replace('jmp', 'nop')

    elif 'nop' in line:
      newcode[i] = newcode[i].replace('nop', 'jmp')

    cpu = CPU(debug_mode=False)
    cpu.load_code(newcode)

    try:
      cpu.run()
    except RepeatedInstructionError:
      pass
    except EndOfCodeError:
      return cpu.acc

if __name__ == '__main__':
  data = readlines(rpath('day08.txt'))
  print(part1(data))
  print(part2(data))
