from itertools import product

from util.helpers import readlines, rpath, tpath
from intcode import Intcode


def part1(data):
  cpu = Intcode()
  cpu.load_program(data)
  cpu.ram[1] = 12
  cpu.ram[2] = 2
  cpu.run()
  return cpu.ram[0]

def part2(data, target):
  cpu = Intcode()
  cpu.load_program(data)

  for i, j in product(range(100), range(100)):
    cpu.reset()
    cpu.ram[1] = i
    cpu.ram[2] = j
    cpu.run()
    if cpu.ram[0] == target:
      return 100 * i + j


if __name__ == '__main__':
  data = readlines(rpath('day02.txt', 'aoc2019'), sep=',', conv=int)

  print(part1(data))
  print(part2(data, 19690720))
