import re
import timeit
from itertools import product


def row_diff(row):
  return max(row) - min(row)

def pt1(data):
  return sum([row_diff(line) for line in data])

def pt2(data):
  acc = []
  for line in data:
    for p in (p for p in product(line, repeat=2) if p[0] != p[1]):
      if p[0] % p[1] == 0:
        acc.append(p[0]//p[1])
        break
  return sum(acc)


if __name__ == '__main__':
  with open('day2.txt', 'r') as f:
    data = [[int(x) for x in re.split(r'\s+', line)] for line in f.read().splitlines()]

  pt1_time = timeit.timeit(lambda: pt1(data), number=1000)
  pt2_time = timeit.timeit(lambda: pt1(data), number=1000)
  print(f'pt1: {pt1(data):10} | {pt1_time:0.6f}s')
  print(f'pt2: {pt2(data):10} | {pt2_time:0.6f}s')
