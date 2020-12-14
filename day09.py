from itertools import permutations

from helpers import readlines, rpath, tpath


def sum_of_previous(ls, i, plen=25):
  num = ls[i]
  for n, k in permutations(range(plen+1), 2):
    if n != k and ls[i-n] + ls[i-k] == num:
      return True
  return False

def part1(data):
  for i, n in enumerate(data):
    if i < 25:
      continue

    if not sum_of_previous(data, i, plen=25):
      return n

def part2(ls, n):
  for plen in range(2, len(ls)):
    for i in range(len(ls) - plen):
      chunk = ls[i:i+plen]
      if sum(chunk) == n:
        return min(chunk) + max(chunk)
  return None


if __name__ == '__main__':
  data = readlines(rpath('day09.txt'), conv=int)
  part1_res = part1(data)
  print(part1_res)
  print(part2(data, part1_res))
