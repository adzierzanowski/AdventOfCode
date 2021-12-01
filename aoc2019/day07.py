from itertools import permutations, cycle
from util.helpers import readlines, rpath, tpath

from intcode import Intcode


def part1(data):
  signals = []
  for perm in permutations((0,1,2,3,4)):
    out = 0
    for p in perm:
      cpu = Intcode(inputs=[p, out])
      cpu.load_program(data)
      cpu.run()
      out = cpu.outputs[-1]
    signals.append(out)
  return max(signals)

def part2(data):
  signals = []
  for perm in permutations((5,6,7,8,9)):
    cpus = [Intcode(debug=False, wfi_mode=True, inputs=[p]) for _, p in enumerate(perm)]
    for cpu in cpus:
      cpu.load_program(data)

    out = 0
    i = 0
    while True:
      cpu = cpus[i%5]
      cpu.feed_inputs(out)
      cpu.run()
      out = cpu.outputs[-1]
      if all([cpu.halt for cpu in cpus]):
        break
      i += 1
    signals.append(cpu.outputs[-1])
  return max(signals)


if __name__ == '__main__':
  data = readlines(rpath('day07.txt', 'aoc2019'), sep=',', conv=int)

  print(part1(data))
  print(part2(data))
