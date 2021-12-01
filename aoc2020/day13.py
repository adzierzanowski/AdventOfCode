from functools import reduce
from operator import mul

from util.helpers import readlines, rpath, tpath


def minv(a, b):
  if b == 1:
    return 1

  b0 = b
  x0, x1 = 0, 1

  while a > 1:
    q = a // b
    a, b = b, a % b
    x0, x1 = x1 - q * x0, x0

  return x1 if x1 >= 0 else x1 + b0

def chinese(resmods):
  as_, ns = zip(*resmods)
  p = reduce(mul, ns)
  return sum([a * minv(p//n, n) * (p//n) for a, n in resmods]) % p

def part1(tstmp, buslines):
  t = tstmp
  while True:
    for b in buslines:
      if t % b == 0:
        return (t - tstmp) * b
    t += 1

def part2(buslines):
  maxbus = max(buslines)
  blines = [((b-i)%b, b) for i, b in enumerate(buslines) if b != 0]
  return chinese(blines)


if __name__ == '__main__':
  data = readlines(rpath('day13.txt', 'aoc2020'))
  tstmp = int(data[0])
  buslines1 = [int(x) for x in data[1].split(',') if x != 'x']
  buslines2 = [0 if x == 'x' else int(x) for x in data[1].split(',')]

  print(part1(tstmp, buslines1))
  print(part2(buslines2))
