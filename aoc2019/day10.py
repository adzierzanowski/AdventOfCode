import math

from itertools import cycle
from collections import namedtuple

from util.helpers import readlines, rpath, tpath


'''
Slope pattern:

L         infR           R
      -3L  ^   3R
           |
           |
-1/3L      |      1/3R
           |
<-nanL-----X----------> 0R
           |
1/3L       |       -1/3R
           |
    3L     |    -3R
           V
        -infR
'''

Detection = namedtuple('Detection', ('src', 'dst', 'slope', 'dist'))

def partition(ls, predicate):
  p, q = [], []
  for el in ls:
    p.append(el) if predicate(el) else q.append(el)
  return p, q

def slope(p1, p2):
  dy = p2[1] - p1[1]
  dx = p2[0] - p1[0]

  if dx == 0:
    slp = -math.inf if dy >= 0 else math.inf
  else:
    if dy == 0:
      slp = 0 if dx >= 0 else float('nan')
    else:
      slp = - dy / dx

  return f'{slp}L' if dx < 0 else f'{slp}R'

def slopesort(slopes):
  east, west = partition(slopes, lambda m: m.endswith('R'))
  northeast, southeast = partition(east, lambda m: not m.startswith('-'))
  southwest, northwest = partition(west, lambda m: not m.startswith('-'))

  for ls in (northeast, southeast, southwest, northwest):
    ls.sort(key=lambda m: -float(m[:-1].replace('nan', '0')))

  return northeast + southeast + southwest + northwest

def distance(p1, p2):
  x1, y1 = p1
  x2, y2 = p2
  return (x2-x1)**2 + (y2-y1)**2

def best_monitoring(asteroids):
  return max([(len(set([slope(asteroid, other)
                       for other in asteroids if asteroid != other])), asteroid)
              for asteroid in asteroids])

def part1(asteroids):
  return best_monitoring(asteroids)[0]

def part2(asteroids):
  best = best_monitoring(asteroids)[1]
  dets = [Detection(best, other, slope(best, other), distance(best, other))
          for other in asteroids]
  dets.sort(key=lambda m: -m.dist)
  slopes = set([det.slope for det in dets])

  for i, slp in enumerate(cycle(slopesort(slopes))):
    others = [det for det in dets if det.slope == slp]
    if others:
      try:
        closest = others.pop()
        dets.remove(closest)
      except IndexError:
        pass

    if i == 199:
      x, y = closest.dst
      return 100 * x + y


if __name__ == '__main__':
  data = readlines(rpath('day10.txt', 'aoc2019'))
  asteroids = [(x, y)
               for y, line in enumerate(data)
               for x, char in enumerate(line)
               if char == '#']
  print(part1(asteroids))
  print(part2(asteroids))
