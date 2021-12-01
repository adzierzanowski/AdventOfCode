from functools import reduce

from util.helpers import readlines, rpath, tpath


def part1(data):
  return sum([len(set(s.replace('\n', ''))) for s in data])

def part2(data):
  return sum([len(reduce(lambda x,y: x.intersection(y),
                         [set(line) for line in group.split('\n')]))
              for group in data])


if __name__ == '__main__':
  data = readlines(rpath('day06.txt', 'aoc2020'), sep='\n\n')
  print(part1(data))
  print(part2(data))
