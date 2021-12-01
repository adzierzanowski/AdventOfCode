from math import exp, radians
import time
from os import stat, terminal_size
from util.helpers import readlines, rpath, tpath
from intcode import Intcode
from collections import namedtuple
from PIL import Image
from random import choice

Direction = namedtuple('Direction', ('cmd', 'vec', 'char'))

class Droid:
  STATUS_WALL, STATUS_OK, STATUS_OXY = 0, 1, 2
  STATUS = '#.O'

  N = Direction(1, (0, -1), '^')
  S = Direction(2, (0, 1), 'V')
  W = Direction(3, (-1, 0), '<')
  E = Direction(4, (1, 0), '>')

  def __init__(self, cpu):
    self.cpu = cpu
    self.dir = Droid.S
    self.pos = 0, 0
    self.map = {(0, 0): Droid.STATUS_OK}
    self.dir_history = [self.dir]
    self.last_wall = False
    self.cpu.run()
    self.steps = 0
    self.hotmap = {}

  def changedir(self):
    if self.dir == Droid.S:
      self.dir = Droid.E if self.last_wall else Droid.W
    elif self.dir == Droid.W:
      self.dir = Droid.S if self.last_wall else Droid.N
    elif self.dir == Droid.E:
      self.dir = Droid.N if self.last_wall else Droid.S
    elif self.dir == Droid.N:
      self.dir = Droid.W if self.last_wall else Droid.E
    if self.last_wall:
      self.steps += 1
      self.hotmap[self.pos] = self.steps

  def move(self):
    self.cpu.feed_inputs(self.dir.cmd)
    self.cpu.run()
    status = self.cpu.read_output()[0]

    x, y = self.pos
    dx, dy = self.dir.vec
    newpos = x+dx, y+dy

    if status == Droid.STATUS_WALL:
      self.map[newpos] = status
      self.last_wall = True

    elif status in (Droid.STATUS_OK, Droid.STATUS_OXY):
      self.map[x+dx, y+dy] = status
      self.pos = x+dx, y+dy
      self.last_wall = False

    self.changedir()

  def get_map(self):
    while not self.cpu.halt:
      self.move()
      if self.pos == (0, 0):
        break
    return self.map

def draw_map(map_, export=False):
  minx = min(map_.keys(), key=lambda m: m[0])[0]
  maxx = max(map_.keys(), key=lambda m: m[0])[0]
  miny = min(map_.keys(), key=lambda m: m[1])[1]
  maxy = max(map_.keys(), key=lambda m: m[1])[1]

  print('\x1b[2J\x1b[0;0H', end='')
  for y in range(miny, maxy+1):
    for x in range(minx, maxx+1):
      if (x, y) == (0, 0):
        print('\x1b[38;5;1m', end='')

      elif (x, y) in map_:
        print(Droid.STATUS[map_[x, y]], end='')
      else:
        print(' ', end='')

      if (x, y) == (0, 0):
        print('\x1b[0m', end='')
    print()
  print()

  if export:
    size = (abs(minx)+abs(maxx)+1), (abs(miny)+abs(maxy)+1)
    print(size)
    img = Image.new('RGB', size, 'black')
    pix = img.load()

    for (x, y), status in map_.items():
      if (x, y) == (0, 0):
        pix[x+abs(minx), y+abs(miny)] = (255, 0, 0)
      if status == Droid.STATUS_WALL:
        pix[x+abs(minx), y+abs(miny)] = (64,64,64)
      elif status == Droid.STATUS_OXY:
        pix[x+abs(minx), y+abs(miny)] = (0, 255, 255)
      elif status == Droid.STATUS_OK and (x, y) != (0, 0):
        pix[x+abs(minx), y+abs(miny)] = (0, 128, 64)

    img.save('day15.bmp')

def get_adjacent(map_, sx, sy):
  return [
    pos for pos in
    ((sx-1, sy), (sx+1, sy), (sx, sy-1), (sx, sy+1))
    if map_.get(pos, Droid.STATUS_WALL) in (Droid.STATUS_OK, Droid.STATUS_OXY)]

def find_path(map_, srcpath, dst):
  sx, sy = srcpath[-1]
  if dst == (sx, sy):
    return srcpath

  adjacent = [pos for pos in get_adjacent(map_, sx, sy) if pos not in srcpath]

  path = []
  for adj in adjacent:
    path += find_path(map_, srcpath + [adj], dst)
  return path

def get_map(data):
  cpu = Intcode(debug=False, wfi_mode=True)
  cpu.load_program(data)
  droid = Droid(cpu)
  map_ = droid.get_map()
  return map_

def part1(map_):
  dst = [pos for pos, status in map_.items() if status == Droid.STATUS_OXY][0]
  path = find_path(map_, [(0, 0)], dst)
  return len(path) - 1

def part2(map_):
  oxy = [pos for pos, status in map_.items() if status == Droid.STATUS_OXY][0]
  adjmap = {**map_}

  minutes = 0
  while any([state == Droid.STATUS_OK for _, state in adjmap.items()]):
    for oxy in [pos for pos, status in adjmap.items() if status == Droid.STATUS_OXY]:
      for adj in get_adjacent(map_, *oxy):
        adjmap[adj] = Droid.STATUS_OXY
    minutes += 1

  return minutes


if __name__ == '__main__':
  data = readlines(rpath('day15.txt', 'aoc2019'), conv=int, sep=',')
  map_ = get_map(data)
  print(part1(map_))
  print(part2(map_))
