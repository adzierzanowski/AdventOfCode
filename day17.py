import cProfile
from itertools import product
from helpers import readlines, rpath, tpath


X = 0
Y = 1
Z = 2
W = 3

def maxc(active, coord):
  return max(active, key=lambda x: x[coord])[coord]

def minc(active, coord):
  return min(active, key=lambda x: x[coord])[coord]

def minmaxc(active, coord):
  return minc(active, coord) - 1, maxc(active, coord) + 2

def count_neighbors(active, x, y, z, w=None):
  if w is None:
    prod = product(range(x-1, x+2), range(y-1, y+2), range(z-1, z+2))
  else:
    prod = product(range(x-1, x+2), range(y-1, y+2), range(z-1, z+2), range(w-1, w+2))
  return len([p for p in prod if p in active])

def iterate3d(active):
  new_active = []

  for z in range(minc(active, Z)-1, maxc(active, Z)+2):
    for y in range(minc(active, Y)-1, maxc(active, Y)+2):
      for x in range(minc(active, X)-1, maxc(active, X)+2):
        neighcnt = count_neighbors(active, x, y, z)
        if (x, y, z) in active:
          if neighcnt in (3, 4):
            new_active.append((x, y, z))
        else:
          if neighcnt == 3:
            new_active.append((x, y, z))
  return new_active

def iterate3d(active):
  rngs = [range(*minmaxc(active, c)) for c in (X, Y, Z)]

  new_active = []
  for x, y, z in product(*rngs):
    neighcnt = count_neighbors(active, x, y, z)
    if (x, y, z) in active:
      if neighcnt in (3, 4):
        new_active.append((x, y, z))
    else:
      if neighcnt == 3:
        new_active.append((x, y, z))
  return new_active


def iterate4d(active):
  rngs = [range(*minmaxc(active, c)) for c in (X, Y, Z, W)]
  new_active = []
  for x, y, z, w in product(*rngs):
    neighcnt = count_neighbors(active, x, y, z, w)
    if (x, y, z, w) in active:
      if neighcnt in (3, 4):
        new_active.append((x, y, z, w))
    else:
      if neighcnt == 3:
        new_active.append((x, y, z, w))
  return new_active


def part1(data):
  active = [(x, y, 0)
            for y, line in enumerate(data)
            for x, val in enumerate(line)
            if val == '#']

  a = active
  for i in range(6):
    a = iterate3d(a)
  return len(a)

def part2(data):
  active = [(x, y, 0, 0)
            for y, line in enumerate(data)
            for x, val in enumerate(line)
            if val == '#']
  a = active
  for i in range(6):
    a = iterate4d(a)
  return len(a)


if __name__ == "__main__":
  data = readlines(rpath('day17.txt'))
  print(part1(data))
  print(part2(data))
