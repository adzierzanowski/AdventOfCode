import math

from util.helpers import readlines, rpath, tpath


def get_points(path):
  x = 0
  y = 0

  pts = [(0,0)]
  for p in path:
    dir_, dist = p[0], int(p[1:])
    rng = range(1, dist+1)

    if dir_ == 'U':
      pts += [(x, y+i) for i in rng]
      y += dist
    elif dir_ == 'D':
      pts += [(x, y-i) for i in rng]
      y -= dist
    elif dir_ == 'L':
      pts += [(x-i, y) for i in rng]
      x -= dist
    elif dir_ == 'R':
      pts += [(x+i, y) for i in rng]
      x += dist

  return pts

def dist(p):
  if p == (0, 0):
    return math.inf
  return abs(p[0]) + abs(p[1])

def part1(p1p, p2p):
  pmin = min(set(p1p) & set(p2p), key=lambda p: dist(p))
  return dist(pmin)

def part2(p1p, p2p):
  isect = set(p1p) & set(p2p) - set([(0,0)])
  p1d, p2d = {}, {}

  for i, p in enumerate(p1p):
    if p in isect:
      p1d[p] = i

  for i, p in enumerate(p2p):
    if p in isect:
      p2d[p] = i

  pd = {p: d+p2d[p] for p, d in p1d.items()}

  return min(pd.values())


if __name__ == '__main__':
  data = readlines(rpath('day03.txt', 'aoc2019'), conv=lambda l: l.split(','))
  p1, p2 = data
  p1p = get_points(p1)
  p2p = get_points(p2)

  print(part1(p1p, p2p))
  print(part2(p1p, p2p))
