from itertools import permutations

from util.helpers import readlines, rpath, tpath


def part1(data):
  for seq in permutations(data, 2):
    if sum(seq) == 2020:
      return seq[0] * seq[1]

def part2(data):
  for seq in permutations(data, 3):
    if sum(seq) == 2020:
      return seq[0] * seq[1] * seq[2]


if __name__ == '__main__':
  data = readlines(rpath('day01.txt', 'aoc2020'), conv=int)
  print(part1(data))
  print(part2(data))
