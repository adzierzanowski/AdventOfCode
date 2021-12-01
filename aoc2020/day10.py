from functools import reduce
from operator import mul

from util.helpers import readlines, rpath, tpath, tribonacci


def get_diffs(data):
  path = [0] + sorted(data) + [max(data)+3]
  diffs = [path[i+1] - path[i] for i in range(len(path)-1)]
  return diffs

def part1(data):
  diffs = get_diffs(data)
  return diffs.count(1) * diffs.count(3)

def part2(data):
  diffs = ''.join([str(x) for x in get_diffs(data)])
  ones = [d for d in diffs.split('3') if d not in ('', '1')]

  # Ways we can substitute differences of 1 with differences of 2 or 3
  # (plus 1 for no change at all)
  # 11    -> 2 (11, 2)
  # 111   -> 4 (111, 21, 12, 3)
  # 1111  -> 7 (1111, 211, 112, 22, 31, 13)

  # Sequence of four ones is sufficient for the task
  # but it would be neat if I'd actually find a formula for all cases
  # (see part2_tribonacci)

  sub = {'11': 2, '111': 4, '1111': 7}
  return reduce(mul, [sub[d] for d in ones])

def part2_tribonacci(data):
  # Ok, after some research, someone told me it's a Tribonacci sequence
  # So here's part2 using this function
  diffs = ''.join([str(x) for x in get_diffs(data)])
  ones = [d for d in diffs.split('3') if d not in ('', '1')]
  return reduce(mul, [tribonacci(len(d)) for d in ones])


if __name__ == '__main__':
  data = readlines(rpath('day10.txt', 'aoc2020'), conv=int)
  print(part1(data))
  print(part2(data))
  print(part2_tribonacci(data))
