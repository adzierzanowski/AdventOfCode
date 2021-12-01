from util.helpers import readlines, rpath, tpath
from itertools import product

from intcode import Intcode


def check_beam(cpu, x, y):
  cpu.reset()
  cpu.inputs = [x, y]
  cpu.run()

  return cpu.read_output()[0]

def part1(cpu):
  return sum([check_beam(cpu, x, y) for x, y in product(range(50), range(50))])

def part2(cpu):
  y = 5
  xmin = 3
  xmax = 3

  while True:
    y += 1

    x = xmin
    directly_down = check_beam(cpu, x, y)
    if not directly_down:
      x += 1
      while not check_beam(cpu, x, y):
        x += 1
      xmin = x

    x = xmax
    directly_down = check_beam(cpu, x, y)
    if directly_down:
      x += 1
      while check_beam(cpu, x, y):
        x += 1
      xmax = x

    if xmax - xmin > 100:
      if check_beam(cpu, xmax-100, y+99):
        return 10000 * (xmax-100) + y


if __name__ == '__main__':
  data = readlines(rpath('day19.txt', 'aoc2019'), conv=int, sep=',')
  cpu = Intcode()
  cpu.load_program(data)
  print(part1(cpu))
  print(part2(cpu))
