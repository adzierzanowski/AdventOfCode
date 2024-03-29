from functools import reduce
from operator import mul

from util.helpers import readlines, rpath, tpath


def count_trees(data, dx, dy, startx=0, starty=0):
  x, y = startx, starty
  w, h = len(data[0]), len(data)
  tree_count = 0

  while y + dy < h:
    x += dx
    x %= w
    y += dy
    if data[y][x] == '#':
      tree_count += 1

  return tree_count

def part1(data):
  return count_trees(data, 3, 1)

def part2(data):
  slopes = ((1,1), (3,1), (5,1), (7,1), (1,2))
  return reduce(mul, [count_trees(data, dx, dy) for dx, dy in slopes])


if __name__ == '__main__':
  data = readlines(rpath('day03.txt', 'aoc2020'))
  print(part1(data))
  print(part2(data))
