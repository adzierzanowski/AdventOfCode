from enum import Enum

from helpers import readlines, rpath, tpath


W, N, E, S = 0, 1, 2, 3

class Point:
  def __init__(self, x=0, y=0):
    self.x = x
    self.y = y

  def rotate(self, cw, halfpi):
    if cw:
      halfpi = 4 - halfpi

    if halfpi == 1:
      self.x, self.y = -self.y, self.x
    elif halfpi == 2:
      self.x, self.y = -self.x, -self.y
    elif halfpi == 3:
      self.x, self.y = self.y, -self.x

class Ship:
  def __init__(self):
    self.dir = E
    self.pos = Point()
    self.wp = Point(10, 1)

  def move(self, val):
    c, v, d = val[0], int(val[1:]), self.dir

    if c == 'W' or (c, d) == ('F', W):
      self.pos.x -= v
    elif c == 'N' or (c, d) == ('F', N):
      self.pos.y += v
    elif c == 'E' or (c, d) == ('F', E):
      self.pos.x += v
    elif c == 'S' or (c, d) == ('F', S):
      self.pos.y -= v

    elif c == 'L':
      self.dir = (self.dir - v // 90) % 4
    elif c == 'R':
      self.dir = (self.dir + v // 90) % 4

  def movew(self, val):
    c, v = val[0], int(val[1:])

    if c == 'W':
      self.wp.x -= v
    elif c == 'N':
      self.wp.y += v
    elif c == 'E':
      self.wp.x += v
    elif c == 'S':
      self.wp.y -= v

    elif c == 'F':
      self.pos.x += v * self.wp.x
      self.pos.y += v * self.wp.y

    elif c == 'L':
      self.wp.rotate(False, v // 90 % 4)

    elif c == 'R':
      self.wp.rotate(True, v // 90 % 4)

def task(data, movef):
  ship = Ship()
  for v in data:
    getattr(ship, movef)(v)
  return abs(ship.pos.x) + abs(ship.pos.y)

def part1(data):
  return task(data, 'move')

def part2(data):
  return task(data, 'movew')


if __name__ == "__main__":
  data = readlines(rpath('day12.txt'))
  print(part1(data))
  print(part2(data))
