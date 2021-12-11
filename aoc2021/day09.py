from operator import mul
from functools import reduce
from util.helpers import readlines, rpath, tpath


def adj(x, y):
  return ((x-1, y), (x+1, y), (x, y-1), (x, y+1))

def lowpoints(data):
  hmap = {
    (x, y): int(h) for y, line in enumerate(data) for x, h in enumerate(line)}

  lowp = []
  for (x, y), h in hmap.items():
    if all((h < hmap.get(p, 10) for p in adj(x, y))):
      lowp.append((x, y))

  return lowp, hmap

def part1(data):
  lowp, hmap = lowpoints(data)
  return sum([hmap.get(p)+1 for p in lowp])

def part2(data):
  lowp, hmap = lowpoints(data)
  basins = [[(x, y)] for x, y in lowp]

  for basin in basins:
    for (x, y) in basin:
      adjp = [p for p in adj(x, y)
        if p not in basin and hmap.get(p) not in (9, None)]
      basin += adjp

  return reduce(
    mul, sorted([len(basin) for basin in basins], key=lambda m: -m)[:3])

def get_data():
  return readlines(rpath('day09.txt', 'aoc2021'))


if __name__ == '__main__':
  data = get_data()
  print(part1(data))
  print(part2(data))
