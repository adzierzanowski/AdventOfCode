from functools import reduce
from helpers import readlines


test_data = [
  'abc',
  'a\nb\nc',
  'ab\nac',
  'a\na\na\na',
  'b'
]

def part1(data):
  return sum([len(set(s.replace('\n', ''))) for s in data])

def part2(data):
  return sum([len(reduce(lambda x,y: x.intersection(y),
                         [set(line) for line in group.split('\n')]))
              for group in data])


if __name__ == '__main__':
  data = readlines('day6.txt', sep='\n\n')
  print(part1(data))
  print(part2(data))
