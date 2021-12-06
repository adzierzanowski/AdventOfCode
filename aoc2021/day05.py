from typing import Counter
from util.helpers import readlines, rpath, tpath


def part1(data):
  pts = []
  for line in data:
    start, end = line.split(' -> ')
    sx, sy = [int(x) for x in start.split(',')]
    ex, ey = [int(x) for x in end.split(',')]
    if sx == ex:
      for i in range(min(sy,ey), max(sy,ey)+1):
        pts.append((sx, i))
    elif sy == ey:
      for i in range(min(sx,ex), max(sx,ex)+1):
        pts.append((i, sy))

  return len([v for v in Counter(pts).values() if v > 1])


def part2(data):
  pts = []
  for line in data:
    start, end = line.split(' -> ')
    sx, sy = [int(x) for x in start.split(',')]
    ex, ey = [int(x) for x in end.split(',')]
    if sx == ex:
      for i in range(min(sy,ey), max(sy,ey)+1):
        pts.append((sx, i))
    elif sy == ey:
      for i in range(min(sx,ex), max(sx,ex)+1):
        pts.append((i, sy))
    else:
      s = min(((sx, sy), (ex, ey)), key=lambda m: m[0])
      e = (sx, sy) if s == (ex, ey) else (ex, ey)
      dy = -1 if (e[1] < s[1]) else 1
      for x, y in zip(range(s[0], e[0]+1), range(s[1], e[1]+dy, dy)):
        pts.append((x, y))

  for y in range(10):
    for x in range(10):
      if (x, y) in pts:
        print('x', end='')
      else:
        print('.', end='')
    print()

  return len([v for v in Counter(pts).values() if v > 1])


if __name__ == '__main__':
  data = readlines(rpath('day05.txt', 'aoc2021'))
  print(part1(data))
  print(part2(data))
