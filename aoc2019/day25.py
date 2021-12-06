from util.helpers import readlines, rpath, tpath
from intcode import Intcode


def part1(data):
  cpu = Intcode()
  cpu.set_ascii_mode(True)
  cpu.load_program(data)
  while True:
    try:
      cpu.run()
    except KeyboardInterrupt:
      pass
    print(''.join([chr(c) for c in cpu.read_output()]))


def part2(data):
  pass


if __name__ == '__main__':
  data = readlines(rpath('day25.txt', 'aoc2019'), conv=int, sep=',')
  print(part1(data))
  print(part2(data))
