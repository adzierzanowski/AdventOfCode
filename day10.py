from operator import mul
from functools import reduce
import re
from helpers import readlines, rpath, tpath

def get_diffs(data):
  path = [0] + sorted(data) + [max(data)+3]
  diffs = [path[i+1] - path[i] for i in range(len(path)-1)]
  return diffs

def part1(data):
  diffs = get_diffs(data)
  return diffs.count(1) * diffs.count(3)

def part2(data):
  diffs = get_diffs(data)
  diffs = ''.join([str(x) for x in diffs])
  ones = [d for d in diffs.split('3') if d != '' and d != '1']

  # Ways we can substitute differences of 1 with differences of 2 or 3
  # (plus 1 for no change at all)
  # 11    -> 2  (11, 2)
  # 111   -> 4 (111, 21, 12, 3)
  # 1111  -> 7 (1111, 211, 112, 22, 31, 13)

  # Sequence of four ones is sufficient for the task
  # but it would be neat if I'd actually find a formula for all cases
  sub = {'11':2, '111':4, '1111':7}
  subones = [sub[d] for d in ones]
  return reduce(mul, subones)


if __name__ == "__main__":
  data = readlines(rpath('day10.txt'), conv=int)
  print(part1(data))
  print(part2(data))
