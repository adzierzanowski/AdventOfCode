from itertools import permutations

from helpers import readlines, rpath, tpath


def part1(data):
  for seq in permutations(data, 2):
    if sum(seq) == 2020:
      return seq[0] * seq[1]

def part2(data):
  for seq in permutations(data, 3):
    if sum(seq) == 2020:
      return seq[0] * seq[1] * seq[2]


if __name__ == '__main__':
  data = readlines(tpath('day01.txt'), conv=int)
  print(part1(data))
  print(part2(data))
