from operator import add
import sys

from intcode import Intcode
from util.helpers import readlines, rpath, tpath, readraw


class Robot:
  N = [0, -1]
  S = [0, 1]
  W = [-1, 0]
  E = [1, 0]

  def __init__(self, cpu: Intcode):
    self.cpu = cpu
    self.hull = {}
    self.position = (0, 0)
    self.direction = Robot.N

  def turn_left(self):
    x, y = self.direction
    self.direction = [y, x] if y else [y, -x]

  def turn_right(self):
    x, y = self.direction
    self.direction = [-y, x] if y else [y, x]

  def start(self, init_input):
    self.cpu.run()
    self.move(force=init_input)
    self.cpu.run()
    while not self.cpu.halt:
      self.move()
      self.cpu.run()

  def move(self, force=None):
    if force is not None:
      self.cpu.feed_inputs(force)
      self.cpu.run()
    else:
      new_color, turn = self.cpu.read_output()
      self.hull[self.position] = new_color
      self.turn_right() if turn else self.turn_left()
      self.position = tuple(map(add, self.position, self.direction))
      current_color = self.hull[self.position] if self.position in self.hull else 0
      self.cpu.feed_inputs(current_color)
      self.cpu.run()

  def print_hull(self, with_robot=False, black='.'):
    xmin = min(self.hull.keys(), key=lambda m: m[0])[0]
    ymin = min(self.hull.keys(), key=lambda m: m[1])[1]
    xmax = max(self.hull.keys(), key=lambda m: m[0])[0]
    ymax = max(self.hull.keys(), key=lambda m: m[1])[1]

    for y in range(ymin, ymax+1):
      for x in range(xmin, xmax+1):
        if with_robot and (x, y) == self.position:
          if self.direction == Robot.N:
            print('^', end='')
          elif self.direction == Robot.E:
            print('>', end='')
          elif self.direction == Robot.S:
            print('V', end='')
          elif self.direction == Robot.W:
            print('<', end='')

        elif (x, y) in self.hull:
          print('#' if self.hull[(x, y)] else black, end='')
        else:
          print(' ', end='')
      print()


def part1(data):
  cpu = Intcode(wfi_mode=True, debug=False)
  cpu.load_program(data)
  robot = Robot(cpu)
  robot.start(0)
  return len(robot.hull)

def part2(data):
  cpu = Intcode(wfi_mode=True, debug=False)
  cpu.load_program(data)
  robot = Robot(cpu)
  robot.start(1)
  robot.print_hull(black=' ')

if __name__ == '__main__':
  data = readraw(rpath('day11.txt', 'aoc2019'), sep=',', conv=int)

  print(part1(data))
  part2(data)
