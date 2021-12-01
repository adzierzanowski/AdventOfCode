from util.helpers import readlines, rpath, tpath
from intcode import Intcode


def part1(data):
  cpu = Intcode(inputs=[1], debug=False)
  cpu.load_program(data)
  cpu.run()
  return cpu.outputs[-1]

def part2(data):
  cpu = Intcode(inputs=[2], debug=False)
  cpu.load_program(data)
  cpu.run()
  return cpu.outputs[-1]


if __name__ == '__main__':
  data = readlines(rpath('day09.txt', 'aoc2019'), sep=',', conv=int)

  print(part1(data))
  print(part2(data))
