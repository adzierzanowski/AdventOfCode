import sys

from helpers import readlines
from timeit import timeit


test_data = [
  1721,
  979,
  366,
  299,
  675,
  1456,
]

def part1(data):
  for i, val in enumerate(data):
    for val2 in data[i+1:]:
      if val + val2 == 2020:
        return val * val2

def part2(data):
  for i, val in enumerate(data):
    for j, val2 in enumerate(data[i+1:]):
      for val3 in data[j+1:]:
        if val + val2 + val3 == 2020:
          return val * val2 * val3


if __name__ == '__main__':
  data = readlines('day1.txt', conv=int)
  print(part1(data))
  print(part2(data))
